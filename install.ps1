param(
    [ValidateSet("cpu", "cu118", "cu121", "cu122", "metal")]
    [string]$Backend = "cpu",
    [switch]$Server
)

$indexUrl = "https://abetlen.github.io/llama-cpp-python/whl/$Backend"
$extras = if ($Server) { "[server]" } else { "" }

Write-Host "Installing gemma-talker with backend: $Backend$(if ($Server) { ' (+ server)' })"
pipx install -e ".$extras" --pip-args="--extra-index-url $indexUrl"
