# Skill: git-push

Haz commit y push automático de todos los cambios pendientes al repositorio remoto.

## Pasos

1. **Obtén el estado actual** — ejecuta en paralelo:
   - `git status` — para ver archivos modificados/nuevos/eliminados
   - `git diff HEAD` — para ver el contenido exacto de los cambios
   - `git log --oneline -5` — para ver el estilo de commits recientes del repo

2. **Determina el tipo de cambio** según Conventional Commits:
   - `feat:` — nueva funcionalidad visible para el usuario
   - `fix:` — corrección de un bug
   - `style:` — cambios de CSS/UI sin lógica nueva
   - `refactor:` — reorganización de código sin cambio funcional
   - `content:` — actualizaciones de datos, textos o traducciones
   - `docs:` — solo documentación
   - `chore:` — archivos de configuración, scripts, build

   Elige el tipo que mejor describe el cambio principal. Si hay varios tipos,
   usa el más relevante en el subject y menciona los demás en el body.

3. **Redacta el mensaje de commit** en este formato:
   ```
   <tipo>(<scope opcional>): <descripción corta en español, imperativo, ≤72 chars>

   <body opcional: qué cambió y por qué, si no es obvio por el subject>

   Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
   ```
   - El subject va en español, en imperativo ("Añade", "Corrige", "Actualiza")
   - El scope es opcional: componente afectado (ej. `i18n`, `index`, `disease-data`)
   - No menciones el número de archivos ni detalles de implementación en el subject

4. **Ejecuta los comandos** en orden:
   ```bash
   git add -A
   git commit -m "<mensaje generado>"
   git push
   ```
   Usa HEREDOC para el mensaje si contiene saltos de línea.

5. **Informa el resultado**: muestra el hash del commit y confirma que el push fue exitoso.

## Reglas

- Si `git status` muestra "nothing to commit", infórmalo y no hagas nada más.
- No uses `--no-verify`, `--force` ni flags destructivos.
- Si el push falla (ej. rama sin upstream), sugiere el comando correcto al usuario.
- No pidas confirmación — ejecuta directamente, es la intención del skill.
