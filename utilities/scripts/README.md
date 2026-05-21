# Utilities — Skripte

Dieses Verzeichnis enthält die Python-Skripte, die die generierten Artefakte des Repos (`.obj`, `.glb`, Thumbnails, Kategorie-Readmes, Root-Readme) aus den `.blend`-Quelldateien und Texturen erzeugen. Orchestriert werden sie von den Workflows unter `.github/workflows/`, sie können aber genauso lokal ausgeführt werden.

## Überblick

| Skript | Zweck | Läuft in … |
| --- | --- | --- |
| [`exportOBJ.py`](#exportobjpy) | `.obj`/`.mtl` aus `<Cat>/blender/*.blend` exportieren | Blender (`bpy`) |
| [`exportGLB.py`](#exportglbpy) | `.glb` aus `<Cat>/blender/*.blend` exportieren | Blender (`bpy`) |
| [`renderThumbnail.py`](#renderthumbnailpy) | 250×250 Cycles-JPEG-Thumbnails rendern | Blender (`bpy`) |
| [`createReadme.py`](#createreadmepy) | Pro-Kategorie- und Root-`README.md` erzeugen | Reines Python |
| [`exportOBJ_Verkehrszeichen.py`](#exportobj_verkehrszeichenpy) | Rohlinge nach `Verkehrszeichen/tmp/*.obj` exportieren | Blender (`bpy`) |
| [`retextureOBJ_Verkehrszeichen.py`](#retextureobj_verkehrszeichenpy) | Rohlinge je Textur in `Verkehrszeichen/obj/*.obj` ausfächern | Reines Python |
| [`categories.yml`](#categoriesyml) | Konfiguration für `createReadme.py` | – |

Alle Skripte ermitteln das Repo-Root via GitPython:

```python
runDir = git.Repo(".", search_parent_directories=True).git.rev_parse("--show-toplevel")
```

Sie müssen daher innerhalb des Repos laufen — das aktuelle Arbeitsverzeichnis innerhalb des Repos ist egal.

Blender-Skripte werden über den `--`-Separator aufgerufen:

```bash
blender --background --python <skript>.py -- <argumente>
```

Reine Python-Skripte erhalten ihre Argumente direkt. Im Repo wird Python immer über `uv run` aufgerufen, z. B. `uv run python utilities/scripts/createReadme.py …`. Die nötigen Pakete (`gitpython`, `pyyaml`) stehen in der `pyproject.toml` und werden von `uv` automatisch bereitgestellt.

Für Blender-Skripte gilt das **nicht**: Blender benutzt sein mitgeliefertes Python, nicht die `uv`-Umgebung. Die `pyproject.toml` ist für `bpy`-Skripte irrelevant — `gitpython` muss separat in Blenders Python installiert sein (in der CI passiert das per `uv pip install --system gitpython`).

---

## Generische, kategorisierte Skripte

Diese drei Skripte teilen sich dasselbe CLI-Muster: eine oder mehrere Kategorien als Positional-Argumente, alternativ `--all`. Kategorien werden entweder über ihren Alias (z. B. `Ausleger`) oder über den Verzeichnisnamen (z. B. `Beleuchtung_Ausleger`) angesprochen.

### `exportOBJ.py`

**Zweck.** Öffnet jede `.blend`-Datei einer Kategorie, exportiert `.obj`+`.mtl` nach `<Cat>/obj/`, kopiert `<Cat>/textures/*` nach `<Cat>/obj/textures/` und korrigiert die Texturpfade in den `.mtl`-Dateien.

**Unterstützte Kategorien** (alle außer Verkehrszeichen):

| Alias | Verzeichnis | `triangulate` |
| --- | --- | --- |
| `Abfallbehaelter` | `Abfallbehaelter` | false |
| `Ampeln` | `Ampeln` | true |
| `Ausleger` | `Beleuchtung_Ausleger` | false |
| `Lampen` | `Beleuchtung_Lampen` | false |
| `Masten` | `Beleuchtung_Masten` | false |
| `Wandhalterung` | `Beleuchtung_Wandhalterung` | true |
| `Werbeanlagen` | `Werbeanlagen` | true |

Das `triangulate`-Flag spiegelt das historische Verhalten der früheren `exportOBJ_<Cat>.py`-Skripte (Faces vor dem Export triangulieren oder nicht).

**Export-Parameter.** `forward_axis="NEGATIVE_Y"`, `up_axis="Z"`, `export_materials=True`, `export_triangulated_mesh=<per Kategorie>`, `path_mode="RELATIVE"`.

**Texturpfad-Fixup.** Blenders `path_mode="RELATIVE"` löst Texturpfade relativ zur `.blend`-Datei (die in `<Cat>/blender/` liegt) auf und schreibt daher `../../textures/...` in die `.mtl`. Nach dem Kopieren der Texturen nach `<Cat>/obj/textures/` ist der korrekte relative Pfad jedoch `../textures/...`. Das Skript ersetzt deshalb in jeder erzeugten `.mtl` `"../../"` durch `"../"`.

**Aufruf.**

```bash
blender --background --python utilities/scripts/exportOBJ.py -- Abfallbehaelter
blender --background --python utilities/scripts/exportOBJ.py -- Ampeln Lampen Werbeanlagen
blender --background --python utilities/scripts/exportOBJ.py -- --all
```

### `exportGLB.py`

**Zweck.** Öffnet jede `.blend`-Datei einer Kategorie, exportiert sie als `.glb` nach `<Cat>/glb/` und kopiert `<Cat>/textures/*` nach `<Cat>/glb/textures/`.

**Unterstützte Kategorien.** Identisch zu `exportOBJ.py`, ebenfalls ohne Verkehrszeichen. Das `triangulate`-Flag entfällt — `.glb` wird über den glTF-Exporter mit Standardoptionen geschrieben (`export_format="GLB"`).

**Aufruf.**

```bash
blender --background --python utilities/scripts/exportGLB.py -- Ampeln
blender --background --python utilities/scripts/exportGLB.py -- --all
```

### `renderThumbnail.py`

**Zweck.** Rendert pro Modell ein 250×250 JPEG mit Cycles (64 Samples) nach `<Cat>/thumbs/`.

**Unterstützte Kategorien.** Dieselben sieben wie bei `exportGLB.py`, **plus** Verkehrszeichen (s. u.).

**Standardpfad** (alle Kategorien außer Verkehrszeichen). Für jede `.blend` in `<Cat>/blender/`:

1. Datei öffnen.
2. Render-Engine auf `CYCLES`, Auflösung 250×250, 64 Samples, Output `JPEG`.
3. Aktuelle Szene rendern und nach `<Cat>/thumbs/<modellname>.jpg` schreiben (Leerzeichen werden im Dateinamen durch `_` ersetzt).

Es wird also davon ausgegangen, dass jede `.blend` selbst Kamera, Licht und Welt-Setup für ein verwertbares Thumbnail mitbringt.

**Verkehrszeichen-Sonderpfad.** Statt `<Cat>/blender/*.blend` werden die fertigen `.obj` aus `Verkehrszeichen/obj/` benutzt. Pro `.obj`:

1. `utilities/default.blend` öffnen (liefert Kamera, Licht, HDRI-Welt).
2. `.obj` importieren (`forward_axis="Y"`).
3. Kamera über `view3d.camera_to_view_selected()` auf das Objekt rahmen, dann Brennweite auf `100 mm` setzen (leichtes Ranzoomen).
4. Mit demselben Render-Setup wie oben nach `Verkehrszeichen/thumbs/<signname>.jpg` schreiben.

Dieser Pfad setzt voraus, dass `exportOBJ_Verkehrszeichen.py` + `retextureOBJ_Verkehrszeichen.py` bereits gelaufen sind.

**Aufruf.**

```bash
blender --background --python utilities/scripts/renderThumbnail.py -- Ampeln
blender --background --python utilities/scripts/renderThumbnail.py -- Verkehrszeichen
blender --background --python utilities/scripts/renderThumbnail.py -- --all
```

### `createReadme.py`

**Zweck.** Erzeugt aus `<Cat>/thumbs/` eine Markdown-Tabelle der Modelle und schreibt sie als `<Cat>/README.md`. Mit `--root` wird zusätzlich (oder ausschließlich) das Root-`README.md` aus `categories.yml` regeneriert. Reines Python — kein Blender nötig.

**Pro-Kategorie-Readme.** Jede Datei in `<Cat>/thumbs/` ergibt eine Zeile mit:

- Modellname (Dateiname ohne `.jpg`)
- Eingebettetes Vorschaubild (`thumbs/<name>.jpg`)
- **Falls** `has_glb: true` in `categories.yml`: ein zusätzlicher Link zum [online 3D Viewer](https://3dviewer.net) mit der GLB-URL des Modells (`https://github.com/rostock/3DModels/blob/main/<directory>/glb/<modell>.glb` plus voreingestellten Viewer-Parametern).

Vor der Tabelle stehen `# <display_name>` und der `intro:`-Block aus `categories.yml`.

**Root-Readme.** Mit `--root` werden alle Einträge aus `categories.yml` zu einer Übersichtsliste geschrieben (`README.md` im Repo-Root). Kategorien, deren Verzeichnis mit `Beleuchtung_` beginnt, werden als Unterpunkte unter „Beleuchtung“ gruppiert; alle anderen erscheinen als Top-Level-Einträge.

**Aufruf.**

```bash
uv run python utilities/scripts/createReadme.py Abfallbehaelter
uv run python utilities/scripts/createReadme.py Ampeln Lampen Werbeanlagen
uv run python utilities/scripts/createReadme.py --all
uv run python utilities/scripts/createReadme.py --root
uv run python utilities/scripts/createReadme.py --all --root
```

Mindestens eines von `<kategorien>`, `--all`, `--root` muss angegeben werden. `--all` und Positional-Kategorien sind gegenseitig ausschließend.

---

## Verkehrszeichen-spezifische Skripte

Verkehrszeichen haben eine eigene Pipeline, weil jede Schildform (Kreis, Quadrat, Dreieck, …) nur **eine** „Rohling“-`.blend` ist und die einzelnen Schilder nur durch unterschiedliche Texturen entstehen.

### `exportOBJ_Verkehrszeichen.py`

**Zweck.** Öffnet jede Rohling-`.blend` in `Verkehrszeichen/blender/` und exportiert sie als `.obj`+`.mtl` nach `Verkehrszeichen/tmp/<shape>.obj`. Identische Export-Parameter wie `exportOBJ.py` (`forward_axis="NEGATIVE_Y"`, `up_axis="Z"`, `export_materials=True`, `path_mode="RELATIVE"`).

Diese `.obj`-Dateien referenzieren `rohling.jpg` als Textur und dienen ausschließlich als Vorlagen für den nächsten Schritt.

**Aufruf.**

```bash
blender --background --python utilities/scripts/exportOBJ_Verkehrszeichen.py
```

### `retextureOBJ_Verkehrszeichen.py`

**Zweck.** Fächert jeden Rohling in eine `.obj`/`.mtl` pro tatsächlichem Verkehrszeichen aus.

**Vorgehen** (für jede `<shape>.obj` in `Verkehrszeichen/tmp/`):

1. Pro Texturdatei in `Verkehrszeichen/textures/<shape>/` (außer `rohling.jpg`):
   - `tmp/<shape>.obj` nach `obj/<signname>.obj` kopieren.
   - `tmp/<shape>.mtl` nach `obj/<signname>.mtl` kopieren.
   - `<signname>.jpg` nach `obj/textures/<shape>/<signname>.jpg` kopieren.
2. In jeder neuen `.obj` die `mtllib`-Referenz von `<shape>.mtl` auf `<signname>.mtl` umschreiben.
3. In jeder neuen `.mtl` `rohling.jpg` auf `<signname>.jpg` umschreiben (und Windows-Pfad-Reste `..\\` entschärfen).
4. Zum Schluss `Verkehrszeichen/tmp/` löschen.

Ein neues Verkehrszeichen anzulegen heißt also in der Regel: eine `.jpg` in den richtigen `Verkehrszeichen/textures/<shape>/`-Ordner legen — keine neue `.blend` nötig.

**Aufruf.**

```bash
uv run python utilities/scripts/retextureOBJ_Verkehrszeichen.py
```

---

## Konfiguration

### `categories.yml`

Steuert ausschließlich `createReadme.py`. Pro Kategorie ein Block:

| Schlüssel | Bedeutung |
| --- | --- |
| `<key>` | Kurz-Alias, auf der CLI von `createReadme.py` akzeptiert |
| `directory` | Top-Level-Verzeichnis der Kategorie im Repo |
| `display_name` | H1-Titel des Kategorie-Readmes und Linktext im Root-Readme |
| `has_glb` | Falls `true`, bekommt das Kategorie-Readme eine zusätzliche „3D-Modell“-Spalte mit Viewer-Link |
| `intro` | Markdown-Block zwischen H1 und der „## Modelle“-Tabelle |

Die Kategorienlisten der drei Blender-Skripte (`exportOBJ.py`, `exportGLB.py`, `renderThumbnail.py`) sind aus historischen Gründen separat im jeweiligen Skript-Modul gepflegt. Eine neue Kategorie muss daher an allen drei Stellen **und** in `categories.yml` ergänzt werden.

---

## Typische Reihenfolge

Eine vollständige Regenerierung einer Standard-Kategorie:

```bash
blender --background --python utilities/scripts/exportOBJ.py       -- Abfallbehaelter
blender --background --python utilities/scripts/exportGLB.py       -- Abfallbehaelter
blender --background --python utilities/scripts/renderThumbnail.py -- Abfallbehaelter
uv run python utilities/scripts/createReadme.py Abfallbehaelter
```

Für Verkehrszeichen entfällt `exportGLB.py`, dafür kommt der Retexture-Schritt zwischen OBJ-Export und Thumbnail-Rendering:

```bash
blender --background --python utilities/scripts/exportOBJ_Verkehrszeichen.py
uv run python utilities/scripts/retextureOBJ_Verkehrszeichen.py
blender --background --python utilities/scripts/renderThumbnail.py -- Verkehrszeichen
uv run python utilities/scripts/createReadme.py Verkehrszeichen
```

Anmerkung zu Abhängigkeiten: Blender benutzt sein **mitgeliefertes** Python, nicht die `uv`-Umgebung. Damit `import git` innerhalb von `bpy`-Skripten funktioniert, muss `gitpython` im Blender-Python installiert sein (in der CI per `uv pip install --system gitpython`). Für die reinen Python-Skripte (`createReadme.py`, `retextureOBJ_Verkehrszeichen.py`) liefert `uv run` die in `pyproject.toml` deklarierten Pakete automatisch — kein `--with` nötig.
