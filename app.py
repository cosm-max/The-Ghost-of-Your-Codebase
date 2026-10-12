from flask import Flask, jsonify, request, send_from_directory
from analyzer.engine import analyze, score
from ghost.voice import speak, verdict

app = Flask(__name__, static_folder="static")
MAX_CHARS = 20000


@app.get("/")
def index():
    return send_from_directory("static", "index.html")


@app.post("/api/review")
def review():
    code = (request.get_json(silent=True) or {}).get("code", "")
    if not isinstance(code, str) or not code.strip():
        return jsonify(error="Paste some Python code first."), 400
    if len(code) > MAX_CHARS:
        return jsonify(error=f"Keep it under {MAX_CHARS} characters."), 413
    findings = analyze(code)
    s = score(findings)
    return jsonify(score=s, verdict=verdict(s), findings=[
        {"line": f.line, "rule": f.rule, "severity": f.severity, "message": speak(f)}
        for f in findings])


if __name__ == "__main__":
    app.run(debug=True)
