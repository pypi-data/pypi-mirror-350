# Configuration

## OpenAPI Server Configuration

Create a `config.yaml` file in the `biocontext/config` directory:

```yaml
schemas:
  - name: example-server
    url: https://api.example.com/openapi.json
    type: json
    base: https://api.example.com
```
