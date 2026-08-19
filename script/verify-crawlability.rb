#!/usr/bin/env ruby
# frozen_string_literal: true

# Verifies the BUILT site is internally consistent: every internal link resolves
# without a redirect, sitemap.xml entries are valid and indexable, robots.txt
# paths correspond to something real, and cases.md's featured_ids all name a
# real case. Catches the class of regression where a page moves/renames (and a
# link, a sitemap entry, or a robots.txt rule is left pointing at the old
# location) or a featured id is mistyped (and the featured section quietly
# renders short instead of failing).
#
# Usage:
#   bundle exec jekyll build
#   bundle exec ruby script/verify-crawlability.rb [path-to-built-site]
#
# Default built-site path: ./_site. Exits non-zero (and lists every failure) if
# any check fails. Reads the local build output plus cases.md/_projects source
# for the featured-id check — no network access.

require 'nokogiri'
require 'yaml'
require 'set'
require 'uri'

ROOT = File.expand_path('..', __dir__)
SITE_DIR = File.expand_path(ARGV[0] || '_site', ROOT)

unless Dir.exist?(SITE_DIR)
  warn "error: '#{SITE_DIR}' not found. Run `bundle exec jekyll build` first."
  exit 1
end

config = YAML.safe_load(File.read(File.join(ROOT, '_config.yml')))
SITE_HOST = URI.parse(config.fetch('url')).host

# Pages that are deliberately indexable but excluded from the sitemap by design
# (documented at the point they're declared, e.g. book/index.html's frontmatter
# comment: an attribution interstitial, not content meant to rank).
SITEMAP_EXEMPT_PATHS = ['/book/'].freeze

# robots.txt paths that are intentionally defensive against paths that must
# never exist in the build output (git/build internals), not references to
# real content — so "does it resolve" doesn't apply to them.
ROBOTS_INFRASTRUCTURE_PATHS = ['/.git/', '/_site/'].freeze

failures = []

# ---- normalize + resolve a URL/href to a built-site outcome ----------------

def internal_path(href, base_path)
  return nil if href.nil? || href.empty?
  return nil if href.start_with?('mailto:', 'tel:', 'javascript:', '#')

  uri = begin
    URI.join("https://#{SITE_HOST}#{base_path}", href)
  rescue URI::Error
    return nil
  end
  return nil if uri.host && uri.host != SITE_HOST

  uri.path.empty? ? '/' : uri.path
end

# Resolution mirrors GitHub Pages' observed behavior: a directory-style path
# resolves only with its trailing slash; the same path without one 301s.
def resolve(path, site_dir)
  fs_path = File.join(site_dir, path)
  if path.end_with?('/')
    File.file?(File.join(fs_path, 'index.html')) ? :ok : :not_found
  elsif File.file?(fs_path)
    :ok
  elsif File.file?(File.join(fs_path, 'index.html'))
    :redirect
  else
    :not_found
  end
end

# ---- load every built page, index redirect-stub / noindex pages ------------

html_files = Dir.glob(File.join(SITE_DIR, '**', '*.html'))
pages = {} # path -> Nokogiri::HTML doc
html_files.each do |file|
  relative = file.delete_prefix(SITE_DIR + File::SEPARATOR).tr('\\', '/')
  path = '/' + relative.sub(/index\.html\z/, '')
  pages[path] = Nokogiri::HTML5(File.read(file, encoding: 'UTF-8'))
end

redirect_stub_paths = Set.new
noindex_paths = Set.new
pages.each do |path, doc|
  metas = doc.css('meta')
  refresh = metas.find { |m| m['http-equiv'].to_s.downcase == 'refresh' }
  redirect_stub_paths << path if refresh
  robots_meta = metas.find { |m| m['name'].to_s.downcase == 'robots' }
  noindex_paths << path if robots_meta && robots_meta['content'].to_s.downcase.include?('noindex')
end

# ---- check every internal <a href> across the built site -------------------

reachable = Set.new
queue = ['/']
link_count = 0

pages.each do |src_path, doc|
  doc.css('a[href]').each do |a|
    target = internal_path(a['href'], src_path)
    next if target.nil?

    link_count += 1

    case resolve(target, SITE_DIR)
    when :not_found
      failures << "internal 404: #{src_path} links to #{target} (#{a['href']}), no such page"
    when :redirect
      failures << "internal redirect: #{src_path} links to #{target} (#{a['href']}), missing trailing slash causes a 301"
    end

    failures << "internal redirect: #{src_path} links to #{target}, which is a redirect stub — link the final target directly" if redirect_stub_paths.include?(target)
  end
end

# BFS reachability from the home page, following only links that resolve cleanly.
until queue.empty?
  current = queue.shift
  next if reachable.include?(current)
  reachable << current
  doc = pages[current]
  next unless doc

  doc.css('a[href]').each do |a|
    target = internal_path(a['href'], current)
    next if target.nil? || reachable.include?(target)
    queue << target if resolve(target, SITE_DIR) == :ok
  end
end

# ---- sitemap.xml -------------------------------------------------------------

sitemap_file = File.join(SITE_DIR, 'sitemap.xml')
sitemap_locs = Set.new
if File.file?(sitemap_file)
  sitemap_doc = Nokogiri::XML(File.read(sitemap_file, encoding: 'UTF-8'))
  sitemap_doc.remove_namespaces!
  sitemap_doc.css('url > loc').each do |loc|
    uri = URI.parse(loc.text.strip)
    path = uri.path
    sitemap_locs << path

    case resolve(path, SITE_DIR)
    when :not_found
      failures << "invalid sitemap URL: #{path} does not resolve to a built page"
    when :redirect
      failures << "invalid sitemap URL: #{path} is missing a trailing slash and would redirect"
    end

    failures << "indexability/sitemap mismatch: sitemap lists #{path}, which is a redirect stub" if redirect_stub_paths.include?(path)
    failures << "indexability/sitemap mismatch: sitemap lists #{path}, which is marked noindex" if noindex_paths.include?(path)
  end
else
  failures << 'invalid sitemap URL: _site/sitemap.xml does not exist'
end

reachable.each do |path|
  next unless pages.key?(path) # only built HTML pages are sitemap candidates, not PDFs/assets
  next if redirect_stub_paths.include?(path) || noindex_paths.include?(path)
  next if SITEMAP_EXEMPT_PATHS.include?(path)
  next if sitemap_locs.include?(path)

  failures << "indexability/sitemap mismatch: #{path} is reachable and indexable but missing from sitemap.xml"
end

# ---- robots.txt --------------------------------------------------------------

robots_file = File.join(SITE_DIR, 'robots.txt')
if File.file?(robots_file)
  File.readlines(robots_file, encoding: 'UTF-8').each do |line|
    line = line.strip
    next if line.empty? || line.start_with?('#')

    directive, value = line.split(':', 2).map(&:strip)
    case directive&.downcase
    when 'sitemap'
      path = URI.parse(value).path
      failures << "unresolved robots.txt path: Sitemap: #{value} does not resolve" unless resolve(path, SITE_DIR) == :ok
    when 'disallow', 'allow'
      next if value.nil? || value.empty? || value == '/'
      next if ROBOTS_INFRASTRUCTURE_PATHS.include?(value)

      fs_target = File.join(SITE_DIR, value.chomp('/'))
      failures << "unresolved robots.txt path: #{directive}: #{value} does not correspond to anything in the built site" unless File.exist?(fs_target)
    end
  end
else
  failures << 'unresolved robots.txt path: _site/robots.txt does not exist'
end

# ---- cases.md featured_ids ----------------------------------------------------

# cases.md resolves its featured_ids list against the projects collection
# through a guarded Liquid loop (`{% if case %}`) that silently drops any id
# matching no case: the section renders short and the build stays green.
# Checked against source front matter, not the built site's URLs — the
# `:name` permalink slugifies endeavour_id (dots become hyphens), so a
# built-path check would need to duplicate that rule instead of asking the
# same question the Liquid loop asks: does any case carry this endeavour_id.
cases_source = File.read(File.join(ROOT, 'cases.md'), encoding: 'UTF-8')
featured_ids_match = cases_source.match(/featured_ids\s*=\s*"([^"]*)"/)
if featured_ids_match
  known_endeavour_ids = Dir.glob(File.join(ROOT, '_projects', '*.md')).filter_map do |file|
    _, front_matter, = File.read(file, encoding: 'UTF-8').split(/^---\s*$/, 3)
    YAML.safe_load(front_matter.to_s)&.[]('endeavour_id')
  end

  if known_endeavour_ids.empty?
    # _projects/ is gitignored and staged from the private cases pipeline before
    # the real build. A clean worktree/clone has none, and Dir.glob above then
    # returns nothing — which would otherwise read every featured id as
    # unresolved. That's a spurious failure, not a real one, so skip instead of
    # failing; but skip loudly, since a silent skip is the same defect class
    # this guard exists to catch.
    puts 'featured id check skipped: no _projects/*.md staged (cases pipeline not run in this worktree/clone).'
  else
    featured_ids_match[1].split(',').map(&:strip).each do |id|
      unless known_endeavour_ids.include?(id)
        failures << "unresolved featured id: cases.md's featured_ids names '#{id}', which matches no _projects/*.md endeavour_id"
      end
    end
  end
else
  failures << "unresolved featured id: could not find featured_ids in cases.md — guard needs updating to match"
end

# ---- report -------------------------------------------------------------------

puts "Scanned #{pages.size} built pages, #{link_count} internal links, #{sitemap_locs.size} sitemap entries."

if failures.empty?
  puts 'crawlability check passed.'
  exit 0
else
  failures.uniq.sort.each { |f| warn "FAIL: #{f}" }
  warn "\n#{failures.uniq.size} crawlability check failure(s)."
  exit 1
end
