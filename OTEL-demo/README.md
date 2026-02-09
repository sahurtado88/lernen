Probar

for i in {1..200}; do curl -s http://localhost:8000/work >/dev/null; done

brew install hey
hey -z 30s -c 20 http://localhost:8000/work
