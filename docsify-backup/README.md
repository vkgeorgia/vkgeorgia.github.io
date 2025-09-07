# Docsify Backup

Этот архив содержит состояние проекта до перехода на Jekyll.

## Содержимое архива:
- `index.html` - оригинальный Docsify index.html
- `_config.yml` - оригинальная конфигурация Jekyll (которая не использовалась)
- `Gemfile` - оригинальный Gemfile
- `docsify-restore-instructions.md` - инструкции по восстановлению Docsify

## Как вернуться к Docsify:

1. Удалите Jekyll файлы:
   - `_layouts/`
   - `_includes/`
   - `_sass/`
   - `_data/`
   - `.nojekyll` (если есть)

2. Восстановите файлы из архива:
   - Скопируйте `index.html` в корень проекта
   - Скопируйте `_config.yml` и `Gemfile` (если нужно)

3. Создайте файл `.nojekyll` в корне проекта для отключения Jekyll на GitHub Pages

4. Удалите front matter из всех markdown файлов (если он был добавлен)

Дата создания архива: $(Get-Date)

