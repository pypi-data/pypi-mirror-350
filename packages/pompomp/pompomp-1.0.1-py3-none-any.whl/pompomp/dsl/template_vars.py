"""
Template Variables Reference for DSL / Oh My Posh Segments.

This module centralizes the complete list of available variables that can be
used inside templates and DSL blocks (e.g. [.Shell], [.UserName], etc.).

Variables are organized by category:
- Global & dynamic variables (e.g., .UserName, .Segments.Contains)
- Segment-specific variables (e.g., .Full, .Patch for languages)
- Source control variables (e.g., .BranchStatus, .HEAD for git)
- System-related variables (e.g., .Battery, .Shell, .Time)

Each segment is described with:
- Its name and category (language, git, system, etc.)
- A list of variable names, types, and descriptions

These variables are used to generate prompt segments in Oh My Posh themes,
and are available to be queried or documented through the `show-vars` CLI command.
"""
OMP_CLI_SEGMENTS = {
    "meta": {
        "name": "CLI",
    },
    "angular": {
        "name": "Angular",
        "description": "Display the currently active Angular CLI version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "argocd": {
        "name": "ArgoCD Context",
        "description": "Display the current ArgoCD context name, user and/or server.",
        "vars": [
            {"name": ".Name", "type": "string", "description": "the current context name"},
            {"name": ".Server", "type": "string", "description": "the server of the current context"},
            {"name": ".User", "type": "string", "description": "the user of the current context"},
        ],
    },
    "aurelia": {
        "name": "Aurelia",
        "description": "Display the currently active Aurelia version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "bazel": {
        "name": "Bazel",
        "description": "Display the currently active Bazel version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
            {"name": ".Icon", "type": "string", "description": "the icon representing Bazel's logo"},
        ],
    },
    "buf": {
        "name": "Buf",
        "description": "Display the currently active Buf CLI version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "bun": {
        "name": "Bun",
        "description": "Display the currently active Bun CLI version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "cmake": {
        "name": "Cmake",
        "description": "Display the currently active Cmake version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "deno": {
        "name": "Deno",
        "description": "Display the currently active Deno CLI version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "docker": {
        "name": "Docker",
        "description": "Display the current Docker context. Will not be active when using the default context.",
        "vars": [
            {"name": ".Context", "type": "string", "description": "the current active context"},
        ],
    },
    "firebase": {
        "name": "Firebase",
        "description": "Display the current active Firebase project.",
        "vars": [
            {"name": ".Project", "type": "string", "description": "the currently active project"},
        ],
    },
    "flutter": {
        "name": "Flutter",
        "description": "Display the currently active flutter version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "gitversion": {
        "name": "GitVersion",
        "description": "Display the GitVersion version. We strongly recommend using GitVersion Portable for this.",
        "warning": "The GitVersion CLI can be a bit slow, causing the prompt to feel slow. This is why we cache the "
                   "value for 30 minutes by default.",
        "vars": [],
    },
    "helm": {
        "name": "Helm",
        "description": "Display the version of helm",
        "vars": [
            {"name": ".Version", "type": "string", "description": "Helm cli version"},
        ],
    },
    "kubernetes": {
        "name": "Kubernetes",
        "description": "Display the currently active Kubernetes context name and namespace name.",
        "vars": [
            {"name": ".Context", "type": "string", "description": "the current kubectl context"},
            {"name": ".Namespace", "type": "string", "description": "the current kubectl context namespace"},
            {"name": ".User", "type": "string", "description": "the current kubectl context user"},
            {"name": ".Cluster", "type": "string", "description": "the current kubectl context cluster"},
        ],
    },
    "maven": {
        "name": "Maven",
        "description": "Display the currently active Maven version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "nerdbank.gitversioning": {
        "name": "Nerdbank.GitVersioning",
        "description": "Display the Nerdbank.GitVersioning version.",
        "warning": "This only works with the gfortran compiler.",
        "vars": [
            {"name": ".Version", "type": "string", "description": "the current version"},
            {"name": ".AssemblyVersion", "type": "string", "description": "the current assembly version"},
            {"name": ".AssemblyInformationalVersion", "type": "string",
             "description": "the current assembly informational version"},
            {"name": ".NuGetPackageVersion", "type": "string", "description": "the current nuget package version"},
            {"name": ".ChocolateyPackageVersion", "type": "string",
             "description": "the current chocolatey package version"},
            {"name": ".NpmPackageVersion", "type": "string", "description": "the current npm package version"},
            {"name": ".SimpleVersion", "type": "string", "description": "the current simple version"},
        ],
    },
    "nixshell": {
        "name": "Nix Shell",
        "description": "Displays the nix shell status if inside a nix-shell environment.",
        "vars": [
            {"name": ".Type", "type": "string", "description": "the type of nix shell, can be pure, impure or unknown"},
        ],
    },
    "npm": {
        "name": "NPM",
        "description": "Display the currently active npm version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "nx": {
        "name": "Nx",
        "description": "Display the currently active Nx version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "pnpm": {
        "name": "PNPM",
        "description": "Display the currently active pnpm version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "quasar": {
        "name": "Quasar",
        "description": "Display the currently active Quasar CLI version. Only rendered when the current or parent "
                       "folder contains a quasar.config or quasar.config.js file.",
        "vars": {
            "quasar.properties": [
                {"name": ".Full", "type": "string", "description": "the full version"},
                {"name": ".Major", "type": "string", "description": "major number"},
                {"name": ".Minor", "type": "string", "description": "minor number"},
                {"name": ".Patch", "type": "string", "description": "patch number"},
                {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
                {"name": ".Error", "type": "string",
                 "description": "error encountered when fetching the version string"},
                {"name": ".Vite", "type": "Dependency", "description": "the vite dependency, if found"},
                {"name": ".AppVite", "type": "Dependency", "description": "the @quasar/app-vite dependency, if found"},
            ],
            "quasar.dependency": [
                {"name": ".Version", "type": "string", "description": "the full version"},
                {"name": ".Dev", "type": "boolean", "description": "development dependency or not"},
            ],
        },
    },
    "react": {
        "name": "React",
        "description": "Display the currently active React version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "svelte": {
        "name": "Svelte",
        "description": "Display the currently active Svelte version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "talosctlcontext": {
        "name": "Talosctl Context",
        "description": "Displays the currently active Talosctl context name.",
        "vars": [
            {"name": ".Context", "type": "string", "description": "the current talosctl context"},
        ],
    },
    "tauri": {
        "name": "Tauri",
        "description": "Display the currently active Tauri version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "terraformcontext": {
        "name": "Terraform Context",
        "description": "Display the currently active Terraform Workspace name.",
        "vars": [
            {"name": ".WorkspaceName", "type": "string", "description": "is the current workspace name"},
            {"name": ".Version", "type": "string", "description": "terraform version (set fetch_version to true)"},
        ],
    },
    "ui5tooling": {
        "name": "UI5 Tooling",
        "description": "Display the active UI5 tooling version (global or local if present).",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "umbraco": {
        "name": "Umbraco",
        "description": "Display current Umbraco Version if found inside the current working directory.",
        "vars": [
            {"name": ".Modern", "type": "boolean",
             "description": "a boolean to detemine if this is modern Umbraco V9+ using modern .NET or if its legacy "
                            "Umbraco using .NET Framework"},
            {"name": ".Version", "type": "string", "description": "the version of umbraco found"},
        ],
    },
    "unity": {
        "name": "Unity",
        "description": "Display the currently active Unity and C# versions.",
        "vars": [
            {"name": ".UnityVersion", "type": "string", "description": "the Unity version"},
            {"name": ".CSharpVersion", "type": "string", "description": "the C# version"},
        ],
    },
    "xmake": {
        "name": "XMake",
        "description": "Display the currently active xmake version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "yarn": {
        "name": "Yarn",
        "description": "Display the currently active yarn version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
}

OMP_CLOUD_SEGMENTS = {
    "meta": {
        "name": "CLOUD",
    },
    "aws": {
        "name": "AWS Context",
        "description": "Display the currently active AWS profile and region.",
        "vars": [
            {"name": ".Profile", "type": "string", "description": "the currently active profile"},
            {"name": ".Region", "type": "string", "description": "the currently active region"},
        ],
    },
    "azure": {
        "name": "Azure Subscription",
        "description": "Display the currently active Azure subscription information.",
        "vars": [
            {"name": ".EnvironmentName", "type": "string", "description": "Azure environment name"},
            {"name": ".HomeTenantID", "type": "string", "description": "home tenant id"},
            {"name": ".ID", "type": "string", "description": "subscription id"},
            {"name": ".IsDefault", "type": "boolean", "description": "is the default subscription or not"},
            {"name": ".Name", "type": "string", "description": "subscription name"},
            {"name": ".State", "type": "string", "description": "subscription state"},
            {"name": ".TenantID", "type": "string", "description": "tenant id"},
            {"name": ".TenantDisplayName", "type": "string", "description": "tenant name"},
            {"name": ".User.Name", "type": "string", "description": "user name"},
            {"name": ".User.Type", "type": "string", "description": "user type"},
            {"name": ".Origin", "type": "string",
             "description": "where we received the information from, can be CLI or PWSH"},
        ],
    },
    "azuredevcli": {
        "name": "Azure Developer CLI",
        "description": "Display the currently active environment in the Azure Developer CLI.",
        "vars": [
            {"name": ".DefaultEnvironment", "type": "string", "description": "Azure Developer CLI environment name"},
            {"name": ".Version", "type": "number", "description": "Config version number"},
        ],
    },
    "azurefunctions": {
        "name": "Azure Functions",
        "description": "Display the currently active Azure Functions CLI version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "cds": {
        "name": "CDS (SAP CAP)",
        "description": "Display the active CDS CLI version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
            {"name": ".HasDependency", "type": "bool", "description": "a flag if @sap/cds was found in package.json"},
        ],
    },
    "cloudfoundry": {
        "name": "Cloud Foundry",
        "description": "Display the active Cloud Foundry CLI version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "gcp": {
        "name": "GCP Context",
        "description": "Display the currently active GCP project, region and account",
        "vars": [
            {"name": ".Project", "type": "string", "description": "the currently active project"},
            {"name": ".Account", "type": "string", "description": "the currently active account"},
            {"name": ".Region", "type": "string", "description": "default region for the active context"},
            {"name": ".Error", "type": "string",
             "description": "contains any error messages generated when trying to load the GCP config"},
        ],
    },
    "pulumi": {
        "name": "Pulumi",
        "description": "Display the currently active pulumi logged-in user, url and stack.",
        "warning": "This requires a pulumi binary in your PATH and will only show in directories that contain a "
                   "Pulumi.yaml file.",
        "vars": [
            {"name": ".Stack", "type": "string", "description": "the current stack name"},
            {"name": ".User", "type": "string", "description": "is the current logged in user"},
            {"name": ".Url", "type": "string", "description": "the URL of the state where pulumi stores resources"},
        ],
    },
    "sitecore": {
        "name": "Sitecore",
        "description": "Display current Sitecore environment. Will not be active when sitecore.json and user.json don't "
                       "exist.",
        "vars": [
            {"name": ".EndpointName", "type": "string", "description": "name of the current Sitecore environment"},
            {"name": ".CmHost", "type": "string", "description": "host of the current Sitecore environment"},
        ],
    },
}

OMP_LANGUAGES_SEGMENTS = {
    "meta": {
        "name": "Languages",
    },
    "crystal": {
        "name": "Crystal",
        "description": "Display the currently active crystal version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "dart": {
        "name": "Dart",
        "description": "Display the currently active dart version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "dotnet": {
        "name": "Dotnet",
        "description": "Display the currently active dart version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".Prerelease", "type": "string", "description": "prerelease info text"},
            {"name": ".BuildMetadata", "type": "string", "description": "build metadata"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".SDKVersion", "type": "string",
             "description": "the SDK version in global.json when fetch_sdk_version is true"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "elixir": {
        "name": "Elixir",
        "description": "Display the currently active elixir version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "fortran": {
        "name": "Fortran",
        "description": "Display the currently active fortran compiler version.",
        "warning": "This only works with the gfortran compiler.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "golang": {
        "name": "Golang",
        "description": "Display the currently active golang version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "haskell": {
        "name": "Haskell",
        "description": "Display the currently active Glasgow Haskell Compiler (GHC) version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
            {"name": ".StackGhc", "type": "boolean", "description": "true if stack ghc was used, otherwise false"},
        ],
    },
    "java": {
        "name": "Java",
        "description": "Display the currently active java version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "julia": {
        "name": "Julia",
        "description": "Display the currently active julia version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "kotlin": {
        "name": "Kotlin",
        "description": "Display the currently active Kotlin version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "lua": {
        "name": "Lua",
        "description": "Display the currently active Lua or LuaJIT version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
            {"name": ".Executable", "type": "string", "description": "the executable used to fetch the version"},
        ],
    },
    "mojo": {
        "name": "Mojo",
        "description": "Display the currently active version of Mojo and the name of the Magic virtual environment.",
        "vars": [
            {"name": ".Venv", "type": "string", "description": "the virtual environment name (if present)"},
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "nim": {
        "name": "Nim",
        "description": "Display the currently active Nim version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "node": {
        "name": "Node",
        "description": "Display the currently active Node.js version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
            {"name": ".PackageManagerName", "type": "string",
             "description": "the package manager name (npm, yarn or pnpm) when setting fetch_package_manager to true"},
            {"name": ".PackageManagerIcon", "type": "string",
             "description": "the PNPM, Yarn, or NPM icon when setting fetch_package_manager to true"},
            {"name": ".Mismatch", "type": "boolean",
             "description": "true if the version in .nvmrc is not equal to .Full"},
            {"name": ".Expected", "type": "string", "description": "the expected version set in .nvmrc"},
        ],
    },
    "ocaml": {
        "name": "Ocaml",
        "description": "Display the currently active OCaml version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".Prerelease", "type": "string", "description": "channel name"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "perl": {
        "name": "Perl",
        "description": "Display the currently active perl version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "php": {
        "name": "PHP",
        "description": "Display the currently active php version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "python": {
        "name": "Python",
        "description": "Display the currently active python version and virtualenv. Supports conda, virtualenv and pyenv"
                       " (if python points to pyenv shim).",
        "vars": [
            {"name": ".Venv", "type": "string", "description": "the virtual environment name (if present)"},
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "r": {
        "name": "R",
        "description": "Display the currently active R version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "ruby": {
        "name": "Ruby",
        "description": "Display the currently active ruby version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "rust": {
        "name": "Rust",
        "description": "Display the currently active rust version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".Prerelease", "type": "string", "description": "channel name"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "swift": {
        "name": "Swift",
        "description": "Display the currently active Swift version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "v": {
        "name": "V",
        "description": "Display the currently active V version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version (e.g., \"0.4.9\")"},
            {"name": ".Major", "type": "string", "description": "major number (e.g., \"0\")"},
            {"name": ".Minor", "type": "string", "description": "minor number (e.g., \"4\")"},
            {"name": ".Patch", "type": "string", "description": "patch number (e.g., \"9\")"},
            {"name": ".Commit", "type": "string", "description": "commit hash (e.g., \"b487986\")"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "vala": {
        "name": "Vala",
        "description": "Display the currently active vala version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
    "zig": {
        "name": "Zig",
        "description": "Display the currently active zig version.",
        "vars": [
            {"name": ".Full", "type": "string", "description": "the full version"},
            {"name": ".Major", "type": "string", "description": "major number"},
            {"name": ".Minor", "type": "string", "description": "minor number"},
            {"name": ".Patch", "type": "string", "description": "patch number"},
            {"name": ".Prerelease", "type": "string", "description": "prerelease identifier"},
            {"name": ".BuildMetadata", "type": "string", "description": "build identifier"},
            {"name": ".URL", "type": "string", "description": "URL of the version info / release notes"},
            {"name": ".InProjectDir", "type": "bool",
             "description": "whether the working directory is within a Zig project"},
            {"name": ".Error", "type": "string", "description": "error encountered when fetching the version string"},
        ],
    },
}

OMP_SOURCE_CONTROL_SEGMENTS = {
    "meta": {
        "name": "Source Control",
    },
    "git": {
        "name": "Git",
        "description": "Display git information when in a git repository. Also works for subfolders. "
                       "For maximum compatibility, make sure your git executable is up-to-date (when branch or status "
                       "information is incorrect for example).",
        "vars": {
            "git.properties": [
                {"name": ".RepoName", "type": "string", "description": "the repo folder name"},
                {"name": ".Working", "type": "Status", "description": "changes in the worktree (see below)"},
                {"name": ".Staging", "type": "Status", "description": "staged changes in the work tree (see below)"},
                {"name": ".HEAD", "type": "string",
                 "description": "the current HEAD context (branch/rebase/merge/...)"},
                {"name": ".Ref", "type": "string", "description": "the current HEAD reference (branch/tag/...)"},
                {"name": ".Behind", "type": "int", "description": "commits behind of upstream"},
                {"name": ".Ahead", "type": "int", "description": "commits ahead of upstream"},
                {"name": ".BranchStatus", "type": "string",
                 "description": "the current branch context (ahead/behind string representation)"},
                {"name": ".Upstream", "type": "string", "description": "the upstream name (remote)"},
                {"name": ".UpstreamGone", "type": "boolean", "description": "whether the upstream is gone (no remote)"},
                {"name": ".UpstreamIcon", "type": "string",
                 "description": "the upstream icon (based on the icons above)"},
                {"name": ".UpstreamURL", "type": "string",
                 "description": "the upstream URL for use in hyperlinks in templates: {{ url .UpstreamIcon .UpstreamURL }}"},
                {"name": ".StashCount", "type": "int", "description": "the stash count"},
                {"name": ".WorktreeCount", "type": "int", "description": "the worktree count"},
                {"name": ".IsWorkTree", "type": "boolean", "description": "if in a worktree repo or not"},
                {"name": ".IsBare", "type": "boolean",
                 "description": "if in a bare repo or not, only set when fetch_bare_info is set to true"},
                {"name": ".Dir", "type": "string", "description": "the repository's root directory"},
                {"name": ".Kraken", "type": "string",
                 "description": "a link to the current HEAD in GitKraken for use in hyperlinks in templates {{ url .HEAD .Kraken }}"},
                {"name": ".Commit", "type": "Commit", "description": "HEAD commit information (see below)"},
                {"name": ".Detached", "type": "boolean", "description": "true when the head is detached"},
                {"name": ".Merge", "type": "boolean", "description": "true when in a merge"},
                {"name": ".Rebase", "type": "Rebase",
                 "description": "contains the relevant information when in a rebase"},
                {"name": ".CherryPick", "type": "boolean", "description": "true when in a cherry pick"},
                {"name": ".Revert", "type": "boolean", "description": "true when in a revert"},
                {"name": ".LatestTag", "type": "string", "description": "the latest tag name"},
            ],
            "git.status": [
                {"name": ".Unmerged", "type": "int", "description": "number of unmerged changes"},
                {"name": ".Deleted", "type": "int", "description": "number of deleted changes"},
                {"name": ".Added", "type": "int", "description": "number of added changes"},
                {"name": ".Modified", "type": "int", "description": "number of modified changes"},
                {"name": ".Untracked", "type": "int", "description": "number of untracked changes"},
                {"name": ".Changed", "type": "boolean", "description": "if the status contains changes or not"},
                {"name": ".String", "type": "string", "description": "a string representation of the changes above"},
            ],
            "git.commit": [
                {"name": ".Author", "type": "User", "description": "the author of the commit (see below)"},
                {"name": ".Committer", "type": "User", "description": "the committer of the commit (see below)"},
                {"name": ".Subject", "type": "string", "description": "the commit subject"},
                {"name": ".Timestamp", "type": "time", "description": "Time the commit timestamp"},
                {"name": ".Sha", "type": "string", "description": "the commit SHA1"},
                {"name": ".Refs", "type": "Refs", "description": "the commit references"},
            ],
            "git.user": [
                {"name": ".Name", "type": "string", "description": "the user's name"},
                {"name": ".Email", "type": "string", "description": "the user's email"},
            ],
            "git.refs": [
                {"name": ".Heads", "type": "[]string", "description": "branches"},
                {"name": ".Tags", "type": "[]string", "description": "commit's tags"},
                {"name": ".Remotes", "type": "[]string", "description": "remote references"},
            ],
            "git.rebase": [
                {"name": ".Current", "type": "int", "description": "the current rebase step"},
                {"name": ".Total", "type": "int", "description": "the total number of rebase steps"},
                {"name": ".HEAD", "type": "string", "description": "the current HEAD"},
                {"name": ".Onto", "type": "string", "description": "the branch we're rebasing onto"},
            ],
        },
    },
}

OMP_SYSTEM_SEGMENTS = {
    "meta": {
        "name": "System",
    },
    "battery": {
        "name": "Battery",
        "description": "Battery displays the remaining power percentage for your battery.",
        "warning": "The segment is not supported and automatically disabled on Windows when WSL 1 is detected. "
                   "Works fine with WSL 2.",
        "vars": [
            {"name": ".State", "type": "struct", "description": "the battery state, has a .String function"},
            {"name": ".Current", "type": "float64", "description": "Current (momentary) charge rate (in mW)."},
            {"name": ".Full", "type": "float64", "description": "Last known full capacity (in mWh)"},
            {"name": ".Design", "type": "float64", "description": "Reported design capacity (in mWh)"},
            {"name": ".ChargeRate", "type": "float64",
             "description": "Current (momentary) charge rate (in mW). It is always non-negative, consult .State field to"
                            " check whether it means charging or discharging (on some systems this might be always 0 if "
                            "the battery doesn't support it)"},
            {"name": ".Voltage", "type": "float64", "description": "Current voltage (in V)"},
            {"name": ".DesignVoltage", "type": "float64",
             "description": "Design voltage (in V). Some systems (e.g. macOS) do not provide a separate value for this. "
                            "In such cases, or if getting this fails, but getting Voltage succeeds, this field will have"
                            " the same value as Voltage, for convenience"},
            {"name": ".Percentage", "type": "float64", "description": "the current battery percentage"},
            {"name": ".Error", "type": "string",
             "description": "the error in case fetching the battery information failed"},
            {"name": ".Icon", "type": "string", "description": "the icon based on the battery state"},
        ],
    },
    "command": {
        "name": "Command",
        "description": "Command allows you run an arbitrary shell command. Be aware it spawn a new process to fetch the "
                       "result, meaning it will not be able to fetch session based context (look at abusing environment "
                       "variables for that). When the command errors or returns an empty string, this segment isn't rendered.",
        "warning": "While powerful, it tends to take a lot of time executing the command on PowerShell. Even with "
                   "–noprofile it's noticeably slower compared to sh. It's advised to look at using environment variables "
                   "when using PowerShell.",
        "vars": [
            {"name": ".Output", "type": "string", "description": "the output of the command or script."},
        ],
    },
    "executiontime": {
        "name": "Execution Time",
        "description": "Displays the execution time of the previously executed command.",
        "vars": [
            {"name": ".Ms", "type": "number", "description": "the execution time in milliseconds"},
            {"name": ".FormattedMs", "type": "string", "description": "the formatted value based on the style above"},
        ],
    },
    "os": {
        "name": "OS",
        "description": "Display OS specific info - defaults to Icon.",
        "vars": [
            {"name": ".Icon", "type": "string", "description": "The OS icon"},
        ],
    },
    "path": {
        "name": "Path",
        "description": "Display the current path.",
        "vars": [
            {"name": ".Path", "type": "string", "description": "the current directory (based on the style property)"},
            {"name": ".Parent", "type": "string",
             "description": "the current directory's parent folder which ends with a path separator (designed for use "
                            "with style folder, it is empty if .Path contains only one single element)"},
            {"name": ".RootDir", "type": "boolean", "description": "true if we're at the root directory (no parent)"},
            {"name": ".Location", "type": "string", "description": "the current directory (raw value)"},
            {"name": ".StackCount", "type": "int", "description": "the stack count"},
            {"name": ".Writable", "type": "boolean",
             "description": "is the current directory writable by the user or not"},
        ],
    },
    "project": {
        "name": "Project",
        "description": "Display the current version of your project defined in the package file.",
        "vars": [
            {"name": ".Type", "type": "string",
             "description": "The type of project: node, cargo, python, mojo, php, dart, nuspec, dotnet, julia, powershell"},
            {"name": ".Version", "type": "string", "description": "The version of your project"},
            {"name": ".Target", "type": "string",
             "description": "The target framework/language version of your project"},
            {"name": ".Name", "type": "string", "description": "The name of your project"},
            {"name": ".Error", "type": "string",
             "description": "The error context when we can't fetch the project info"},
        ],
    },
    "session": {
        "name": "Session",
        "description": "Show the current user and host name.",
        "vars": [
            {"name": ".UserName", "type": "string", "description": "the current user's name"},
            {"name": ".HostName", "type": "string", "description": "the current computer's name"},
            {"name": ".SSHSession", "type": "boolean", "description": "active SSH session or not"},
            {"name": ".Root", "type": "boolean", "description": "are you a root/admin user or not"},
        ],
    },
    "shell": {
        "name": "Shell",
        "description": "Show the current shell name (zsh, PowerShell, bash, ...).",
        "vars": [
            {"name": ".Name", "type": "string", "description": "the shell name"},
            {"name": ".Version", "type": "string", "description": "the shell version"},
        ],
    },
    "statuscode": {
        "name": "Status Code",
        "description": "Displays the last known status code and/or the reason that the last command failed.",
        "vars": [
            {"name": ".Code", "type": "number", "description": "the last known exit code (command or pipestatus)"},
            {"name": ".String", "type": "string",
             "description": "the formatted status codes using status_template and status_separator"},
            {"name": ".Error", "type": "boolean",
             "description": "true if one of the commands has an error (validates on command status and pipestatus)"},
        ],
    },
    "sysinfo": {
        "name": "System Info",
        "description": "Display SysInfo.",
        "vars": [
            {"name": ".PhysicalTotalMemory", "type": "int", "description": "is the total of used physical memory"},
            {"name": ".PhysicalAvailableMemory", "type": "int",
             "description": "is the total available physical memory (i.e. the amount immediately available to processes)"},
            {"name": ".PhysicalFreeMemory", "type": "int",
             "description": "is the total of free physical memory (i.e. considers memory used by the system for any "
                            "reason [e.g. caching] as occupied)"},
            {"name": ".PhysicalPercentUsed", "type": "float64",
             "description": "is the percentage of physical memory in usage"},
            {"name": ".SwapTotalMemory", "type": "int", "description": "is the total of used swap memory"},
            {"name": ".SwapFreeMemory", "type": "int", "description": "is the total of free swap memory"},
            {"name": ".SwapPercentUsed", "type": "float64", "description": "is the percentage of swap memory in usage"},
            {"name": ".Load1", "type": "float64", "description": "is the current load1 (can be empty on windows)"},
            {"name": ".Load5", "type": "float64", "description": "is the current load5 (can be empty on windows)"},
            {"name": ".Load15", "type": "float64", "description": "is the current load15 (can be empty on windows)"},
            {"name": ".Disks", "type": "[]struct",
             "description": "an array of IOCountersStat object, you can use any property it has e.g. .Disks.disk0.IoTime"},
        ],
    },
    "time": {
        "name": "Time",
        "description": "Show the current timestamp.",
        "vars": [
            {"name": ".Format", "type": "string", "description": "The time format (set via time_format)"},
            {"name": ".CurrentDate", "type": "time", "description": "The time to display (testing purpose)"},
        ],
    },
    "upgrade_notice": {
        "name": "Upgrade notice",
        "description": "Displays when there's an update available for Oh My Posh.",
        "vars": [
            {"name": ".Current", "type": "string", "description": "the current version number"},
            {"name": ".Latest", "type": "string", "description": "the latest available version number"},
        ],
    },
    "windowsregistrykeyquery": {
        "name": "Windows Registry Key Query",
        "description": "Display the content of the requested Windows registry key.",
        "vars": [
            {"name": ".Value", "type": "string", "description": "The result of your query, or fallback if not found."},
        ],
    },
}

TEMPLATE_GLOBAL_VARS = [
    {"name": ".Root", "type": "boolean", "description": "Is the current user root/admin or not"},
    {"name": ".PWD", "type": "string", "description": "Current working directory (~ for $HOME)"},
    {"name": ".AbsolutePWD", "type": "string", "description": "Current working directory (unaltered)"},
    {"name": ".PSWD", "type": "string", "description": "Current non-filesystem working directory in PowerShell"},
    {"name": ".Folder", "type": "string", "description": "Current folder name"},
    {"name": ".Shell", "type": "string", "description": "Current shell name"},
    {"name": ".ShellVersion", "type": "string", "description": "Current shell version"},
    {"name": ".SHLVL", "type": "int", "description": "Current shell level"},
    {"name": ".UserName", "type": "string", "description": "Current user name"},
    {"name": ".HostName", "type": "string", "description": "Current host name"},
    {"name": ".Code", "type": "int", "description": "Last exit code"},
    {"name": ".Jobs", "type": "int", "description": "Number of background jobs (Zsh and PowerShell)"},
    {"name": ".OS", "type": "string", "description": "Operating system"},
    {"name": ".WSL", "type": "boolean", "description": "Are we in a WSL environment?"},
    {"name": ".Templates", "type": "string", "description": "Template rendering result"},
    {"name": ".PromptCount", "type": "int", "description": "Number of prompts invoked in this session"},
    {"name": ".Version", "type": "string", "description": "Oh My Posh version"},
]

TEMPLATE_SEGMENT_CONTEXT = [
    {"name": ".Segment.Index", "type": "int", "description": "Current segment's index"},
    {"name": ".Segment.Text", "type": "string", "description": "Rendered text of the segment"},
]

TEMPLATE_DYNAMIC_VARS = [
    {"name": ".Env.<Var>", "type": "string", "description": "Environment variable"},
    {"name": ".Var.<Var>", "type": "any", "description": "Custom config variable from 'var:' block"},
    {"name": ".Segments.<Segment>", "type": "object", "description": "Access to another segment's properties"},
    {"name": ".Segments.Contains \"Name\"", "type": "bool", "description": "Check if a segment is active"},
]

ALL_GLOBAL_AND_DYNAMIC_VARS = (
        TEMPLATE_GLOBAL_VARS + TEMPLATE_SEGMENT_CONTEXT + TEMPLATE_DYNAMIC_VARS
)


def _handle_dict_vars(vars_block: dict, result: dict, family_name: str, family_map: dict) -> None:
    """
    Add a dictionary of nested segment variables to the flat registry.

    Args:
        vars_block: A dict of subsegments → list of variables.
        result: The output dictionary storing all segment variables.
        family_name: The name of the current family (e.g., "Languages").
        family_map: The map storing segment name → family name.
    """
    for subkey, varlist in vars_block.items():
        result[subkey] = varlist
        family_map[subkey] = family_name


def _handle_list_vars(segment_name: str, vars_block: list, result: dict, family_name: str, family_map: dict) -> None:
    """
    Add a flat list of variables for a given segment into the registry.

    Args:
        segment_name: Name of the segment (e.g., "python", "battery").
        vars_block: A list of variable metadata dicts.
        result: The global result dictionary to populate.
        family_name: The name of the family/group the segment belongs to.
        family_map: The map storing segment name → family name.
    """
    result[segment_name] = vars_block
    family_map[segment_name] = family_name


def rebuild_segment_specific_vars(*families: dict) -> tuple[dict, dict]:
    """
    Flatten and unify all segment-specific variables across families.

    Args:
        *families: One or more dicts describing OMP segment variable families.

    Returns:
        A tuple:
        - dict: Segment name → list of variables.
        - dict: Segment name → family name (used for display).
    """
    segment_vars = {}
    segment_to_family = {}

    for family in families:
        family_meta = family.get("meta", {})
        family_name = family_meta.get("name", "Unknown Family")
        for segment_name, segment_data in family.items():
            if segment_name == "meta":
                continue
            vars_block = segment_data.get("vars")
            if isinstance(vars_block, dict):
                _handle_dict_vars(vars_block, segment_vars, family_name, segment_to_family)
            elif isinstance(vars_block, list):
                _handle_list_vars(segment_name, vars_block, segment_vars, family_name, segment_to_family)
            else:
                raise ValueError(f"Invalid 'vars' structure for segment '{segment_name}'")

    return segment_vars, segment_to_family


# List of all segment families
OMP_ALL_SEGMENT_FAMILIES = [
    OMP_CLI_SEGMENTS,
    OMP_CLOUD_SEGMENTS,
    OMP_LANGUAGES_SEGMENTS,
    OMP_SOURCE_CONTROL_SEGMENTS,
    OMP_SYSTEM_SEGMENTS,
]

# Centralized processing
SEGMENT_SPECIFIC_VARS, SEGMENT_TO_FAMILY = rebuild_segment_specific_vars(*OMP_ALL_SEGMENT_FAMILIES)
