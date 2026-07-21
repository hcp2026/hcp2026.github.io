const path = require("path");
const { spawnSync } = require("child_process");

const script = path.join(__dirname, "render_posters.py");
const result = spawnSync("python3", [script], { stdio: "inherit" });
process.exit(result.status === null ? 1 : result.status);
