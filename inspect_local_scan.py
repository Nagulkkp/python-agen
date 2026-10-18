import json

with open("codebase_scan_result.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Keys:", list(data.keys()))
print(f"Controllers: {len(data['controllers'])}")
print(f"Models: {len(data['models'])}")
print(f"Requests: {len(data['requests'])}")
print(f"Routes: {len(data['routes'])}")
print(f"Services: {len(data['services'])}")
print(f"Workflows: Events={len(data['workflows']['events'])}, Listeners={len(data['workflows']['listeners'])}, Jobs={len(data['workflows']['jobs'])}")
print(f"Middlewares: {len(data['middlewares'])}")
print(f"Recent errors: {len(data['recent_errors'])}")

# Show samples
print("\nSample Controller:")
print(data['controllers'][0])

print("\nSample Model:")
print(data['models'][0])

print("\nSample Request:")
if data['requests']:
    print(data['requests'][0])

print("\nSample Route:")
print(data['routes'][0])

print("\nSample Error:")
if data['recent_errors']:
    print(data['recent_errors'][0])
