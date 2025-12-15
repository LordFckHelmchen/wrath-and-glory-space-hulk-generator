# Use cases

## Table of contents

- [Users](#users)
- [Basic Use Cases](#basic-use-cases)
  - [Generate Space Hulks](#generate-space-hulks)
  - [Review Space Hulks](#review-space-hulks)
  - [Export Space Hulks](#export-space-hulks)
- [Advanced Use Cases](#advanced-use-cases)
  - [Modify Space Hulks](#modify-space-hulks)
  - [Store & Load Space Hulks](#store--load-space-hulks)
  - [Generate Space Hulks from set of existing space hulks](#generate-space-hulks-from-set-of-existing-space-hulks)
  - [Log user actions to optimize UX](#log-user-actions-to-optimize-ux)

## Users

- _Game Master_: Wants to generate a ready-to-use space hulk for his gaming group.
- _Advanced Game Master_: Wants to customize the generated space hulk by adding a background story, a name and fitting
  to fit it to the needs of the gaming group.
- _Maintainer_: Wants to build up a database of good space hulks & provide the best UX with the solution.

## Basic Use Cases

### Generate Space Hulks

```mermaid
flowchart TD
    GM[Game Master] --uses--> GENERATE

    GENERATE --extends to--o GENERATE_WITH_DESCRIPTION

    subgraph GENERATE[Use Case: Generate Space Hulk]
        Generate([Generate space hulk])
        Generate -.contains.-> GenerateEvents([Generate events])
        Generate -.contains.-> GenerateLayout([Generate layout])
    end

    subgraph GENERATE_WITH_DESCRIPTION[Use Case: Generate Space Hulk With Description]
        GenerateWithDescription([Generate with description])
        GenerateWithDescription -.contains.-> GenerateName([Generate name])
        GenerateWithDescription -.contains.-> GenerateDescription([Generate background])
    end
```

### Review Space Hulks

```mermaid
flowchart TD
    GM[Game Master] --uses--> REVIEW

    subgraph REVIEW[Use Case: Review Space Hulk]
        Review([Review space hulk])
        Review -.contains.->ReviewText([Review text])
        Review -.contains.->ReviewGraphics([Review layout])
    end
```

### Export Space Hulks

```mermaid
flowchart TD
    GM[Game Master] --uses--> EXPORT

    subgraph EXPORT[Use Case: Export Space Hulk]
        Export([Export space hulk])
        Export -.contains.-> CreateFile([Create file])
    end
```

## Advanced Use Cases

### Modify Space Hulks

```mermaid
flowchart TD
    GM[Game Master] --extends to--o AdvGM[Advanced Game Master] --uses--> MODIFY

    subgraph MODIFY[Use Case: Modify Space Hulk]
        Modify([Modiy space hulk])
        Modify -.contains.-> ModifyEvents([Modify events])
        Modify -.contains.-> ModifyLayout([Modify layout])
        Modify -.contains.-> ModifyName([Modify name])
        Modify -.contains.-> ModifyDescription([Modify background])
    end
```

### Store & Load Space Hulks

```mermaid
flowchart TD
    GM[Game Master] --extends to--o AdvGM[Advanced Game Master] --uses--> IO

    subgraph IO[Use Case: Store & Load Space Hulk]
        Store([Store with id])
        Load([Load with id])
    end
```

### Generate Space Hulks from set of existing space hulks

Idea: Store "good" space hulks that have been exported by the users and either reuse them or, if the db is big enough,
train an AI model to generate descriptions & names based on the existing ones.

```mermaid
flowchart TD
    GM[Game Master] --uses--> GENERATE_WITH_DESCRIPTION

    GENERATE_WITH_DESCRIPTION --extends to--o GENERATE_FROM_EXISTING --uses--> IO

    subgraph IO[Use Case: Store/Load Space Hulk]
    end

    subgraph GENERATE_WITH_DESCRIPTION[Use Case: Generate Space Hulk With Description]
    end

    subgraph GENERATE_FROM_EXISTING[Use Case: Generate Space Hulk From Existing Data]
        GenerateFromExisting([Generate from existing data])
    end
```

### Log user actions to optimize UX

```mermaid
flowchart TD
    Maintainer --uses--> LOG_UX

    subgraph LOG_UX[Use Case: Log User Actions for UX Optimization]
        LogUX([Log user actions])
        LogUX -.contains.-> LogGenerate([Log space hulk re-/generation])
        LogUX -.contains.-> LogExport([Log space hulk export])
    end
```
