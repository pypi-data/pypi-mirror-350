# Escobar

## Debugging in VSCode

0. Running debug build
npm run build && python3 -m jupyter labextension develop . --overwrite --build=True


1. **Start the watch tasks first**:

   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS)
   - Type "Run Task"
   - Select "Start Development Environment"

   This task runs both:

   - "npm: watch" - Watches and recompiles TypeScript files
   - "jupyter: lab watch" - Watches and rebuilds the extension

2. **Once the watch tasks are running**, start the debug processes:
   - Use the "Debug JupyterLab (Python)" configuration to debug the backend
   - Use the "Debug JupyterLab Extension" configuration to debug the frontend

### TypeScript notes

1. The watch tasks will automatically recompile the TypeScript and rebuild the extension
2. You may need to refresh the JupyterLab page to see the changes
3. For some changes, you might need to restart the debug sessions
