# React + TypeScript + Vite + shadcn/ui

This is a template for a new Vite project with React, TypeScript, and shadcn/ui.

## Development setup

### Running with Docker

The development container is managed through `just`. To start the webapp:

```bash
just up dev
```

This will build the Docker image and start the container with Vite's dev server available at `http://localhost:5173`.

### Installing dependencies locally

Inside the container, `node_modules` are installed in a separate directory (`/deps/node_modules`) and symlinked into the project at startup. This avoids Docker creating a root-owned `node_modules` folder on the host through the bind mount.

However, your editor (e.g. VSCode) relies on a local `node_modules` directory to resolve types and provide autocompletion. You need to install dependencies on the host as well:

```bash
cd webapp
npm ci
```

Both installs are independent: the container uses its own modules from `/deps`, while the host installation is only used by your editor.

## Adding components

To add components to your app, run the following command:

```bash
npx shadcn@latest add button
```

This will place the ui components in the `src/components` directory.

## Using components

To use the components in your app, import them as follows:

```tsx
import { Button } from "@/components/ui/button"
```
