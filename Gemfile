source "https://rubygems.org"

# GitHub Pages (commonmarker) пока требует Ruby < 4. Для локальной сборки:
#   export PATH="/opt/homebrew/opt/ruby@3.3/bin:$PATH"
ruby ">= 3.3", "< 4.0"

# Ruby 3.4+: stdlib-гемы; на 3.3 не мешают
gem "csv"
gem "bigdecimal"

gem "fiddle"
gem "minima"

group :jekyll_plugins do
  # 232+ тянет Jekyll 3.10 и актуальнее стека Pages, чем старые 223 + liquid 4.0.3
  gem "github-pages", "~> 232"
  gem "faraday-retry"
  gem "jekyll-mermaid"
end
