import os
import re
import json

base_dir = os.path.dirname(os.path.abspath(__file__))

def scan_controllers():
    ctrl_dir = os.path.join(base_dir, "app", "Http", "Controllers")
    controllers = []
    if not os.path.exists(ctrl_dir):
        return controllers

    for root, _, files in os.walk(ctrl_dir):
        for f in files:
            if not f.endswith(".php"):
                continue
            path = os.path.join(root, f)
            rel_path = os.path.relpath(path, base_dir).replace("\\", "/")
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as fp:
                    content = fp.read()
            except Exception:
                continue

            class_m = re.search(r"class\s+([A-Za-z0-9_]+)", content)
            class_name = class_m.group(1) if class_m else f[:-4]

            # Public methods
            methods = re.findall(r"public\s+function\s+([A-Za-z0-9_]+)\s*\(([^)]*)\)", content)
            method_list = []
            for m_name, params in methods:
                if m_name == "__construct":
                    continue
                clean_params = ", ".join([p.strip().split("$")[-1] for p in params.split(",") if p.strip()])
                method_list.append({"name": m_name, "params": clean_params})

            # Middleware in constructor
            middlewares = re.findall(r"\$this->middleware\s*\(\s*['\"]([^'\"]+)['\"]", content)

            # Events & jobs fired
            events = re.findall(r"event\s*\(\s*new\s+([A-Za-z0-9_]+)", content)
            jobs = re.findall(r"([A-Za-z0-9_]+)::dispatch\s*\(", content)

            # In-line validation rules: $request->validate([ ... ]) or Validator::make([ ... ])
            validations = []
            v_matches = re.findall(r"\$request->validate\s*\(\s*\[(.*?)\]\s*\)", content, re.DOTALL)
            v_matches += re.findall(r"Validator::make\s*\([^,]+,\s*\[(.*?)\]\s*\)", content, re.DOTALL)
            for vm in v_matches:
                rules = [r.strip().replace("'", "").replace('"', '') for r in vm.split(",") if "=>" in r]
                if rules:
                    validations.extend(rules[:10])

            controllers.append({
                "file": rel_path,
                "class": class_name,
                "methods": method_list,
                "middlewares": list(set(middlewares)),
                "events": list(set(events)),
                "jobs": list(set(jobs)),
                "validations": validations[:12]
            })
    return controllers

def scan_models():
    models_dir = os.path.join(base_dir, "app", "Models")
    models = []
    if not os.path.exists(models_dir):
        return models

    for root, _, files in os.walk(models_dir):
        for f in files:
            if not f.endswith(".php"):
                continue
            path = os.path.join(root, f)
            rel_path = os.path.relpath(path, base_dir).replace("\\", "/")
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as fp:
                    content = fp.read()
            except Exception:
                continue

            class_m = re.search(r"class\s+([A-Za-z0-9_]+)", content)
            class_name = class_m.group(1) if class_m else f[:-4]

            table_m = re.search(r"protected\s+\$table\s*=\s*['\"]([^'\"]+)['\"]", content)
            table_name = table_m.group(1) if table_m else None

            pk_m = re.search(r"protected\s+\$primaryKey\s*=\s*['\"]([^'\"]+)['\"]", content)
            primary_key = pk_m.group(1) if pk_m else None

            # Fillable
            fillable = []
            fill_m = re.search(r"protected\s+\$fillable\s*=\s*\[(.*?)\];", content, re.DOTALL)
            if fill_m:
                fillable = [item.strip().strip("'\"") for item in fill_m.group(1).split(",") if item.strip()]

            # Constants
            constants = re.findall(r"const\s+([A-Za-z0-9_]+)\s*=\s*([^;]+);", content)

            # Relationships
            rels = []
            rel_patterns = [
                (r"return\s+\$this->belongsTo\s*\(\s*([A-Za-z0-9_\\]+)(?:::class)?(?:\s*,\s*['\"]?([A-Za-z0-9_]+)['\"]?)?", "belongsTo"),
                (r"return\s+\$this->hasMany\s*\(\s*([A-Za-z0-9_\\]+)(?:::class)?(?:\s*,\s*['\"]?([A-Za-z0-9_]+)['\"]?)?", "hasMany"),
                (r"return\s+\$this->hasOne\s*\(\s*([A-Za-z0-9_\\]+)(?:::class)?(?:\s*,\s*['\"]?([A-Za-z0-9_]+)['\"]?)?", "hasOne"),
                (r"return\s+\$this->belongsToMany\s*\(\s*([A-Za-z0-9_\\]+)(?:::class)?(?:\s*,\s*['\"]?([A-Za-z0-9_]+)['\"]?)?", "belongsToMany"),
            ]
            for pat, rtype in rel_patterns:
                for match in re.finditer(pat, content):
                    target = match.group(1).strip().split("\\")[-1]
                    extra = match.group(2).strip() if match.group(2) else ""
                    rels.append({"type": rtype, "target": target, "key_or_pivot": extra})

            models.append({
                "file": rel_path,
                "class": class_name,
                "table": table_name,
                "primary_key": primary_key,
                "fillable": fillable[:25],
                "constants": [f"{c[0]} = {c[1].strip()}" for c in constants],
                "relationships": rels
            })
    return models

def scan_requests():
    req_dir = os.path.join(base_dir, "app", "Http", "Requests")
    requests_list = []
    if not os.path.exists(req_dir):
        return requests_list

    for root, _, files in os.walk(req_dir):
        for f in files:
            if not f.endswith(".php"):
                continue
            path = os.path.join(root, f)
            rel_path = os.path.relpath(path, base_dir).replace("\\", "/")
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as fp:
                    content = fp.read()
            except Exception:
                continue

            class_m = re.search(r"class\s+([A-Za-z0-9_]+)", content)
            class_name = class_m.group(1) if class_m else f[:-4]

            rules_m = re.search(r"public\s+function\s+rules\s*\([^)]*\)[^{]*\{([^}]*)\}", content, re.DOTALL)
            rules_text = rules_m.group(1).strip() if rules_m else ""
            
            clean_rules = []
            for line in rules_text.splitlines():
                line = line.strip().replace("'", "").replace('"', '')
                if "=>" in line:
                    clean_rules.append(line.rstrip(",;"))

            requests_list.append({
                "file": rel_path,
                "class": class_name,
                "rules": clean_rules
            })
    return requests_list

def scan_routes():
    routes_dir = os.path.join(base_dir, "routes")
    routes_list = []
    if not os.path.exists(routes_dir):
        return routes_list

    for root, _, files in os.walk(routes_dir):
        for f in files:
            if not f.endswith(".php"):
                continue
            path = os.path.join(root, f)
            rel_path = os.path.relpath(path, base_dir).replace("\\", "/")
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as fp:
                    content = fp.read()
            except Exception:
                continue

            # Route group prefix and middleware
            group_middleware = []
            gm = re.search(r"Route::group\s*\(\s*\[([^\]]+)\]", content)
            if gm:
                m_match = re.search(r"['\"]middleware['\"]\s*=>\s*(?:\[([^\]]+)\]|['\"]([^'\"]+)['\"])", gm.group(1))
                if m_match:
                    group_middleware = [m.strip().strip("'\"") for m in (m_match.group(1) or m_match.group(2)).split(",") if m.strip()]

            # Standard route calls: Route::get('uri', [Ctrl::class, 'action']) or Route::post('uri', 'Ctrl@action')
            pattern = r"Route::(get|post|put|delete|patch|any|match)\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*(?:\[\s*([A-Za-z0-9_\\]+)(?:::class)?\s*,\s*['\"]([A-Za-z0-9_]+)['\"]\s*\]|['\"]([^'\"]+)['\"])"
            for match in re.finditer(pattern, content):
                method = match.group(1).upper()
                uri = match.group(2)
                ctrl1 = match.group(3)
                act1 = match.group(4)
                ctrl2 = match.group(5)
                
                if ctrl1 and act1:
                    ctrl_name = ctrl1.split("\\")[-1]
                    action_name = act1
                elif ctrl2:
                    parts = ctrl2.split("@")
                    ctrl_name = parts[0].split("\\")[-1]
                    action_name = parts[1] if len(parts) > 1 else "index"
                else:
                    ctrl_name = "Closure"
                    action_name = "invoke"

                routes_list.append({
                    "file": rel_path,
                    "method": method,
                    "uri": uri,
                    "controller": ctrl_name,
                    "action": action_name,
                    "middlewares": group_middleware
                })

            # Resource routes: Route::resource('uri', 'Ctrl')
            res_pattern = r"Route::resource\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*(?:['\"]([^'\"]+)['\"]|([A-Za-z0-9_\\]+)::class)"
            for match in re.finditer(res_pattern, content):
                uri = match.group(1)
                ctrl = (match.group(2) or match.group(3) or "").split("\\")[-1]
                routes_list.append({
                    "file": rel_path,
                    "method": "RESOURCE",
                    "uri": uri,
                    "controller": ctrl,
                    "action": "RESTful CRUD (index, store, show, update, destroy)",
                    "middlewares": group_middleware
                })

    return routes_list

def scan_services():
    services_dir = os.path.join(base_dir, "app", "Services")
    services = []
    if not os.path.exists(services_dir):
        return services

    for root, _, files in os.walk(services_dir):
        for f in files:
            if not f.endswith(".php"):
                continue
            path = os.path.join(root, f)
            rel_path = os.path.relpath(path, base_dir).replace("\\", "/")
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as fp:
                    content = fp.read()
            except Exception:
                continue

            class_m = re.search(r"class\s+([A-Za-z0-9_]+)", content)
            class_name = class_m.group(1) if class_m else f[:-4]
            methods = re.findall(r"public\s+function\s+([A-Za-z0-9_]+)", content)
            services.append({
                "file": rel_path,
                "class": class_name,
                "methods": [m for m in methods if m != "__construct"][:10]
            })
    return services

def scan_events_listeners_jobs():
    items = {"events": [], "listeners": [], "jobs": []}
    for category, subfolder in [("events", "app/Events"), ("listeners", "app/Listeners"), ("jobs", "app/Jobs")]:
        folder_path = os.path.join(base_dir, subfolder)
        if not os.path.exists(folder_path):
            continue
        for root, _, files in os.walk(folder_path):
            for f in files:
                if f.endswith(".php"):
                    path = os.path.join(root, f)
                    rel_path = os.path.relpath(path, base_dir).replace("\\", "/")
                    class_name = f[:-4]
                    items[category].append({
                        "file": rel_path,
                        "class": class_name
                    })
    return items

def scan_laravel_logs():
    log_path = os.path.join(base_dir, "storage", "logs", "laravel.log")
    errors = []
    if not os.path.exists(log_path):
        return errors
    try:
        with open(log_path, "r", encoding="utf-8", errors="replace") as fp:
            lines = fp.readlines()
        tail_lines = "".join(lines[-300:])
        blocks = re.split(r"(?=\[\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\])", tail_lines)
        for b in blocks:
            b = b.strip()
            if not b:
                continue
            first_line = b.splitlines()[0]
            if "ERROR" in first_line or "EMERGENCY" in first_line or "Exception" in b:
                errors.append(first_line[:130])
    except Exception:
        pass
    return list(set(errors))[:20]

def scan_middlewares():
    m_dir = os.path.join(base_dir, "app", "Http", "Middleware")
    middlewares = []
    if os.path.exists(m_dir):
        for f in os.listdir(m_dir):
            if f.endswith(".php"):
                middlewares.append({
                    "name": f[:-4],
                    "file": f"app/Http/Middleware/{f}"
                })
    return middlewares

data = {
    "controllers": scan_controllers(),
    "models": scan_models(),
    "requests": scan_requests(),
    "routes": scan_routes(),
    "services": scan_services(),
    "workflows": scan_events_listeners_jobs(),
    "middlewares": scan_middlewares(),
    "recent_errors": scan_laravel_logs()
}

out_file = os.path.join(base_dir, "codebase_scan_result.json")
with open(out_file, "w", encoding="utf-8") as fp:
    json.dump(data, fp)

print(f"COMPLETE: Controllers={len(data['controllers'])}, Models={len(data['models'])}, Routes={len(data['routes'])}, Requests={len(data['requests'])}, Services={len(data['services'])}, Errors={len(data['recent_errors'])}")
