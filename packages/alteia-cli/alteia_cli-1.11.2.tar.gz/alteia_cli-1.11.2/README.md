# `alteia`

CLI for Alteia Platform.

**Usage**:

```console
$ alteia [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-p, --profile TEXT`: Alteia CLI Profile  [env var: ALTEIA_CLI_PROFILE; default: default]
* `--version`: Display the CLI version and exit
* `--verbose`: Display more info during the run
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `configure`: Configure platform credentials.
* `analytics`: Interact with analytics.
* `analytic-configurations`: Interact with configurations of analytics.
* `credentials`: Interact with Docker registry credentials.
* `products`: Interact with products.

## `alteia configure`

Configure platform credentials.

You can configure multiples credential profiles by specifying
a different profile name for each one.

**Usage**:

```console
$ alteia configure [OPTIONS] [PROFILE]
```

**Arguments**:

* `[PROFILE]`: Alteia CLI Profile to configure  [env var: ALTEIA_CLI_PROFILE; default: default]

**Options**:

* `--insecure`: Allow insecure connection for profile, disable SSL certificate verification
* `--help`: Show this message and exit.

## `alteia analytics`

Interact with analytics.

**Usage**:

```console
$ alteia analytics [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `list`: List the analytics.
* `create`: Create a new analytic.
* `unshare`: Unshare an analytic (DEPRECATED: use...
* `share`: Share an analytic (DEPRECATED: use expose...
* `delete`: Delete an analytic.
* `expose`: Expose an analytic
* `unexpose`: Unexpose an analytic
* `list-exposed`: List exposed analytics
* `enable`: Enable an analytic on companies
* `disable`: Disable an analytic on companies
* `list-orderable`: List orderable analytics on a company
* `set-docker-credentials-name`: Set docker credentials name.
* `credentials`: Manage analytics credentials.

### `alteia analytics list`

List the analytics.

**Usage**:

```console
$ alteia analytics list [OPTIONS]
```

**Options**:

* `-n, --limit INTEGER RANGE`: Max number of analytics returned.  [default: 100; x&gt;=1]
* `--all`: If set, display all kinds of analytics (otherwise only custom analytics are displayed).
* `--help`: Show this message and exit.

### `alteia analytics create`

Create a new analytic.

**Usage**:

```console
$ alteia analytics create [OPTIONS]
```

**Options**:

* `--description PATH`: Path of the Analytic description (YAML file).  [required]
* `--company TEXT`: Company identifier.
* `--help`: Show this message and exit.

### `alteia analytics unshare`

Unshare an analytic (DEPRECATED: use unexpose instead)

**Usage**:

```console
$ alteia analytics unshare [OPTIONS] ANALYTIC_NAME
```

**Arguments**:

* `ANALYTIC_NAME`: [required]

**Options**:

* `--version TEXT`: Range of versions in SemVer format. If not provided, all the versions will be unshared.
* `--company TEXT`: Identifier of the company to unshare the analytic with.
* `--domain / --no-domain`: To unshare the analytic with the root company of your domain.

This is equivalent to using the --company option providing
the id of the root company.
Note that if you specifically shared the analytic with a company
of your domain, the analytic will still be shared with that company.  [default: no-domain]
* `--help`: Show this message and exit.

### `alteia analytics share`

Share an analytic (DEPRECATED: use expose instead)

**Usage**:

```console
$ alteia analytics share [OPTIONS] ANALYTIC_NAME
```

**Arguments**:

* `ANALYTIC_NAME`: [required]

**Options**:

* `--version TEXT`: Range of versions in SemVer format. If not provided, all the versions will be shared.
* `--company TEXT`: Identifier of the company to share the analytic with.

When providing the identifier of the root company of your domain,
the analytic is shared with all the companies of the domain
(equivalent to using the --domain option)
* `--domain / --no-domain`: To share the analytic with the root company of your domain.

This has the effect to share the analytic with all the
companies of your domain and is equivalent to using the
--company option providing the id of the root company.  [default: no-domain]
* `--help`: Show this message and exit.

### `alteia analytics delete`

Delete an analytic.

**Usage**:

```console
$ alteia analytics delete [OPTIONS] ANALYTIC_NAME
```

**Arguments**:

* `ANALYTIC_NAME`: [required]

**Options**:

* `--version TEXT`: Version range of the analytic in SemVer format. If not provided, all the versions will be deleted.
* `--help`: Show this message and exit.

### `alteia analytics expose`

Expose an analytic

**Usage**:

```console
$ alteia analytics expose [OPTIONS] ANALYTIC_NAME
```

**Arguments**:

* `ANALYTIC_NAME`: [required]

**Options**:

* `--domain TEXT`: To expose the analytic on the specified domains (comma separated values) if you have the right permissions on these domains.

By default, without providing this option, the analytic will be exposed on your domain if you have the right permissions on it.
* `--help`: Show this message and exit.

### `alteia analytics unexpose`

Unexpose an analytic

**Usage**:

```console
$ alteia analytics unexpose [OPTIONS] ANALYTIC_NAME
```

**Arguments**:

* `ANALYTIC_NAME`: [required]

**Options**:

* `--domain TEXT`: To unexpose the analytic from the specified domains (comma separated values) if you have the right permissions on these domains.

By default, without providing this option, the analytic will be unexposed from your domain if you have the right permissions on it.
* `--help`: Show this message and exit.

### `alteia analytics list-exposed`

List exposed analytics

**Usage**:

```console
$ alteia analytics list-exposed [OPTIONS]
```

**Options**:

* `--all`: If set, display all kinds of analytics (otherwise only custom analytics are displayed).
* `--domain TEXT`: If set, filters exposed analytics on the specified domains (comma separated values) if you have the right permissions on these domains.

By default, without providing this option, it filters on your domain.
* `--help`: Show this message and exit.

### `alteia analytics enable`

Enable an analytic on companies

**Usage**:

```console
$ alteia analytics enable [OPTIONS] ANALYTIC_NAME
```

**Arguments**:

* `ANALYTIC_NAME`: [required]

**Options**:

* `--company TEXT`: Identifier of the company to enable the analytic, or list of such identifiers (comma separated values).

When providing the identifier of the root company of your domain, the analytic is enabled by default for all the companies of the domain (equivalent to using the --domain option).
* `--domain TEXT`: Use this option to make the analytic enabled by default for all companies of the specified domains (comma separated values) (equivalent to using the --company option providing the root company identifier(s) of these domains).

Apart from this default behavior on domain, the analytic can be enabled or disabled separately on each company of the domain.
* `--help`: Show this message and exit.

### `alteia analytics disable`

Disable an analytic on companies

**Usage**:

```console
$ alteia analytics disable [OPTIONS] ANALYTIC_NAME
```

**Arguments**:

* `ANALYTIC_NAME`: [required]

**Options**:

* `--company TEXT`: Identifier of the company to disable the analytic, or list of such identifiers (comma separated values).

When providing the identifier of the root company of your domain, the analytic is disabled by default for all the companies of the domain (equivalent to using the --domain option).
* `--domain TEXT`: Use this option to make the analytic disabled by default for all companies of the specified domains (comma separated values) (equivalent to using the --company option providing the root company identifier(s) of these domains).

Apart from this default behavior on domain, the analytic can be enabled or disabled separately on each company of the domain.
* `--help`: Show this message and exit.

### `alteia analytics list-orderable`

List orderable analytics on a company

**Usage**:

```console
$ alteia analytics list-orderable [OPTIONS] COMPANY_ID
```

**Arguments**:

* `COMPANY_ID`: [required]

**Options**:

* `--all`: If set, display all kinds of analytics (otherwise only custom analytics are displayed).
* `--help`: Show this message and exit.

### `alteia analytics set-docker-credentials-name`

Set docker credentials name.

**Usage**:

```console
$ alteia analytics set-docker-credentials-name [OPTIONS] NAME
```

**Arguments**:

* `NAME`: [required]

**Options**:

* `--version TEXT`: Version of the analytic to update.  [required]
* `--company TEXT`: Short name of the company owning the analytic.  [required]
* `--docker-credentials-name TEXT`: Name of the credentials to use to pull the dockerimage from the registry. The credentials must have been createdbeforehand using the credentials API  [required]
* `--help`: Show this message and exit.

### `alteia analytics credentials`

**Usage**:

```console
$ alteia analytics credentials [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `assign`: Assign credentials to an analytic for a...
* `unassign`: Unassign credentials from an analytic for...
* `list`: List the analytics with configurable...

#### `alteia analytics credentials assign`

Assign credentials to an analytic for a specific version range within a company.

**Usage**:

```console
$ alteia analytics credentials assign [OPTIONS]
```

**Options**:

* `-c, --company TEXT`: The shortname of the company where the credentials are stored.  [required]
* `-n, --name TEXT`: The name of the analytic.  [required]
* `-v, --version TEXT`: The version range on which the credentials will be applied.  [required]
* `--help`: Show this message and exit.

#### `alteia analytics credentials unassign`

Unassign credentials from an analytic for a specific version range within a company.

**Usage**:

```console
$ alteia analytics credentials unassign [OPTIONS]
```

**Options**:

* `-c, --company TEXT`: The shortname of the company where the credentials are stored.  [required]
* `-n, --name TEXT`: The name of the analytic.  [required]
* `-v, --version TEXT`: The version range on which the credentials are applied.  [required]
* `-a, --all`: Bypass the prompt and unassign all credentials for the matching analytic and version range.
* `--help`: Show this message and exit.

#### `alteia analytics credentials list`

List the analytics with configurable credentials for a company and their assigned credentials.

**Usage**:

```console
$ alteia analytics credentials list [OPTIONS]
```

**Options**:

* `-c, --company TEXT`: The shortname of the company where the credentials are configured.  [required]
* `-n, --name TEXT`: The name of an analytic to filter on.
* `--help`: Show this message and exit.

## `alteia analytic-configurations`

Interact with configurations of analytics.

**Usage**:

```console
$ alteia analytic-configurations [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `list`: List the analytic configuration sets and...
* `create`: Create a new configuration set for an...
* `delete`: Delete one or many analytic configuration...
* `update`: Update a configuration set.
* `export`: Export one configuration of a...
* `assign`: Assign an analytic configuration set to a...
* `unassign`: Unassign an analytic configuration set...

### `alteia analytic-configurations list`

List the analytic configuration sets and their configurations.

**Usage**:

```console
$ alteia analytic-configurations list [OPTIONS]
```

**Options**:

* `-n, --limit INTEGER RANGE`: Max number of configuration sets returned.  [default: 100; x&gt;=1]
* `--name TEXT`: Configuration set name (or a part of) to match
* `--analytic TEXT`: Exact analytic name to match
* `--desc`: Print description rather than configurations
* `--help`: Show this message and exit.

### `alteia analytic-configurations create`

Create a new configuration set for an analytic.

A configuration set is composed of configurations, each being applied to
a different version range of the associated analytic.

**Usage**:

```console
$ alteia analytic-configurations create [OPTIONS]
```

**Options**:

* `-c, --config-path PATH`: Path to the Configuration file (YAML or JSON file)  [required]
* `-n, --name TEXT`: Configuration set name (will be prompt if not provided)
* `-a, --analytic TEXT`: Analytic name (will be prompt if not provided)
* `-v, --version-range TEXT`: Version range of the analytic on which this first configuration can be applied
* `-d, --description TEXT`: Configuration set description text
* `--help`: Show this message and exit.

### `alteia analytic-configurations delete`

Delete one or many analytic configuration set(s)
and the associated configuration(s).

**Usage**:

```console
$ alteia analytic-configurations delete [OPTIONS] IDS
```

**Arguments**:

* `IDS`: Identifier of the configuration set to delete, or comma-separated list of configuration set identifiers  [required]

**Options**:

* `--help`: Show this message and exit.

### `alteia analytic-configurations update`

Update a configuration set.
A configuration set is composed of configurations, each being applied
to a different version range of the associated analytic.

To add a new configuration (file), use --add-config with the path to the new
configuration file (YAML or JSON file) and --version-range with the version range
of the analytic you want this new configuration to be applied.

To replace an existing configuration (file), use --replace-config with the path
to the new configuration file (YAML or JSON file) and --version-range with the
exact version range attached to the configuration to replace.

To remove a configuration from a configuration set, use --remove-config
and --version-range with the exact version range attached to the configuration
to remove.

To change the version range for an existing configuration, do an &quot;add&quot; and then
a &quot;remove&quot; (an export may be necessary to do the &quot;add&quot; with the same
configuration file).

**Usage**:

```console
$ alteia analytic-configurations update [OPTIONS] CONFIG_SET_ID
```

**Arguments**:

* `CONFIG_SET_ID`: Identifier of the configuration set to update  [required]

**Options**:

* `-n, --name TEXT`: New configuration set name
* `-d, --description TEXT`: New configuration set description
* `-a, --add-config PATH`: Add new configuration. Specify the path to the new configuration file, and --version-range option with the version range of the analytic you want this new configuration to be applied. Do not use with --replace-config
* `-u, --replace-config PATH`: Replace a configuration. Specify the path to the new configuration file, and --version-range option with the exact version range from the applicable analytic version ranges. Do not use with --add-config
* `-v, --version-range TEXT`: Version range of the analytic on which a configuration can be applied. Must be used with one of --add-config, --replace-config or --remove-config
* `-r, --remove-config TEXT`: Remove a configuration. Specify the exact version range from the applicable analytic version ranges
* `--help`: Show this message and exit.

### `alteia analytic-configurations export`

Export one configuration of a configuration set.
Output can be a JSON or YAML format.

**Usage**:

```console
$ alteia analytic-configurations export [OPTIONS] CONFIG_SET_ID
```

**Arguments**:

* `CONFIG_SET_ID`: Identifier of the configuration set to export value  [required]

**Options**:

* `-v, --version-range TEXT`: Specify the exact version range from the applicable analytic version ranges. Optional if only one configuration exists in the configuration set
* `-f, --format [json|yaml]`: Optional output format  [default: json]
* `-o, --output-path PATH`: Optional output filepath to export the configuration. If the filepath already exists, it will be replaced. If not specified, configuration will be displayed in stdout
* `--help`: Show this message and exit.

### `alteia analytic-configurations assign`

Assign an analytic configuration set to a company.

All analytic configurations that are currently part of this
analytic configuration set (and the potential future ones),
are assigned to the company.

**Usage**:

```console
$ alteia analytic-configurations assign [OPTIONS] CONFIG_SET_ID
```

**Arguments**:

* `CONFIG_SET_ID`: Identifier of the configuration set to assign  [required]

**Options**:

* `-c, --company TEXT`: Identifier of the company the configuration set will be assigned to  [required]
* `--help`: Show this message and exit.

### `alteia analytic-configurations unassign`

Unassign an analytic configuration set from a company.

All configurations currently part of this analytic configuration set,
are unassigned from the company.

**Usage**:

```console
$ alteia analytic-configurations unassign [OPTIONS] CONFIG_SET_ID
```

**Arguments**:

* `CONFIG_SET_ID`: Identifier of the configuration set to unassign  [required]

**Options**:

* `-c, --company TEXT`: Identifier of the company the configuration set is assigned to  [required]
* `--help`: Show this message and exit.

## `alteia credentials`

Interact with Docker registry credentials.

**Usage**:

```console
$ alteia credentials [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `create`: Create a new credential entry.
* `list`: List the existing credentials.
* `delete`: Delete a credential entry by its name.
* `set-credentials`: Set credentials.
* `set-labels`: Set labels.

### `alteia credentials create`

Create a new credential entry.

**Usage**:

```console
$ alteia credentials create [OPTIONS]
```

**Options**:

* `--filepath PATH`: Path of the Credential JSON file.  [required]
* `--company TEXT`: Company identifier.
* `--help`: Show this message and exit.

### `alteia credentials list`

List the existing credentials.

**Usage**:

```console
$ alteia credentials list [OPTIONS]
```

**Options**:

* `--company TEXT`: Company identifier.
* `--help`: Show this message and exit.

### `alteia credentials delete`

Delete a credential entry by its name.

**Usage**:

```console
$ alteia credentials delete [OPTIONS] NAME
```

**Arguments**:

* `NAME`: [required]

**Options**:

* `--help`: Show this message and exit.

### `alteia credentials set-credentials`

Set credentials.

**Usage**:

```console
$ alteia credentials set-credentials [OPTIONS] NAME
```

**Arguments**:

* `NAME`: [required]

**Options**:

* `--company TEXT`: Company identifier.
* `--filepath PATH`: Path of the Credential JSON file.  [required]
* `--help`: Show this message and exit.

### `alteia credentials set-labels`

Set labels.

**Usage**:

```console
$ alteia credentials set-labels [OPTIONS] NAME
```

**Arguments**:

* `NAME`: [required]

**Options**:

* `--company TEXT`: Company identifier.
* `--filepath PATH`: Path of the Labels JSON file.  [required]
* `--help`: Show this message and exit.

## `alteia products`

Interact with products.

**Usage**:

```console
$ alteia products [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `list`: List the products
* `cancel`: Cancel a running product.
* `logs`: Retrieve the logs of a product.

### `alteia products list`

List the products

**Usage**:

```console
$ alteia products list [OPTIONS]
```

**Options**:

* `-n, --limit INTEGER RANGE`: Max number of products returned  [default: 10; x&gt;=1]
* `--analytic TEXT`: Analytic name
* `--company TEXT`: Company identifier
* `--status [pending|processing|available|rejected|failed]`: Product status
* `--all`: If set, display also the products from platform analytics (otherwise only products from custom analytics are displayed).
* `--help`: Show this message and exit.

### `alteia products cancel`

Cancel a running product.

**Usage**:

```console
$ alteia products cancel [OPTIONS] PRODUCT_ID
```

**Arguments**:

* `PRODUCT_ID`: [required]

**Options**:

* `--help`: Show this message and exit.

### `alteia products logs`

Retrieve the logs of a product.

**Usage**:

```console
$ alteia products logs [OPTIONS] PRODUCT_ID
```

**Arguments**:

* `PRODUCT_ID`: [required]

**Options**:

* `-f, --follow`: Follow logs.
* `--help`: Show this message and exit.
