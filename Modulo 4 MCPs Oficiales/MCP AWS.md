# AWS MCP Servers

## Información

| | |
|---|---|
| **Duración** | 45 minutos |
| **Nivel** | Intermedio |
| **Requisitos** | Cuenta AWS, AWS CLI configurado |
| **Riesgo** | Alto (configurable a solo lectura) |

---

## Objetivos de Aprendizaje

Al completar esta sección podrás:

- [ ] Configurar AWS MCP con permisos limitados
- [ ] Usar el modo solo lectura para exploración segura
- [ ] Ejecutar comandos AWS CLI desde Claude
- [ ] Analizar costos de infraestructura
- [ ] Acceder a documentación y best practices de AWS

---

AWS es la plataforma cloud más usada. Con MCPs oficiales puedes **gestionar tu infraestructura cloud conversando con Claude**.

---

## Catálogo de AWS MCPs

| Servidor | Función | Nivel de riesgo |
|----------|---------|-----------------|
| **AWS API** | Ejecutar cualquier comando AWS CLI | Alto (configurable) |
| **AWS Knowledge** | Documentación y best practices | Solo lectura |
| **AWS CDK** | Guía de CDK y CloudFormation | Medio |
| **AWS Cost Analysis** | Análisis de costos | Solo lectura |

---

## 1. AWS API MCP

### Configuración segura

```json
{
  "mcpServers": {
    "aws-api": {
      "command": "uvx",
      "args": ["awslabs.aws-api-mcp-server@latest"],
      "env": {
        "AWS_PROFILE": "mi-perfil",
        "AWS_REGION": "eu-west-1",
        "READ_OPERATIONS_ONLY": "true",
        "ALLOWED_SERVICES": "s3,ec2,lambda"
      }
    }
  }
}
```

### Variables de entorno críticas

| Variable | Función | Recomendación |
|----------|---------|---------------|
| `AWS_PROFILE` | Perfil de credenciales | Usa perfil con permisos limitados |
| `AWS_REGION` | Región por defecto | Tu región principal |
| `READ_OPERATIONS_ONLY` | Limitar a solo lectura | **"true" para empezar** |
| `ALLOWED_SERVICES` | Servicios permitidos | Lista explícita |

### Tools disponibles

| Tool | Función |
|------|---------|
| `execute_aws_command` | Ejecutar comandos AWS CLI |
| `get_execution_plan` | Obtener plan paso a paso |

### Ejemplos de uso

```
Usuario: "Lista todos los buckets de S3"
Claude ejecuta: aws s3 ls

Usuario: "Describe las instancias EC2 en producción"
Claude ejecuta: aws ec2 describe-instances --filters "Name=tag:Environment,Values=production"

Usuario: "¿Cuántas funciones Lambda tengo?"
Claude ejecuta: aws lambda list-functions --query 'length(Functions)'
```

> ⚠️ **Nunca** uses tu perfil de administrador. Crea un perfil IAM específico con permisos mínimos.

---

## 2. AWS Knowledge MCP (Servidor Remoto)

Este MCP es **remoto** - se conecta a servidores de AWS, no ejecuta nada local.

```json
{
  "mcpServers": {
    "aws-knowledge": {
      "url": "https://knowledge-mcp.global.api.aws",
      "type": "http"
    }
  }
}
```

### Qué proporciona

- Documentación oficial de AWS
- Best practices de arquitectura
- Guías de seguridad
- Ejemplos de código

**Ejemplo**: "¿Cómo debo configurar un bucket S3 para hosting estático de forma segura?"

---

## 3. AWS CDK MCP

```json
{
  "mcpServers": {
    "aws-cdk": {
      "command": "uvx",
      "args": ["awslabs.cdk-mcp-server@latest"]
    }
  }
}
```

### Tools disponibles

| Tool | Función |
|------|---------|
| `cdk_synth` | Sintetizar template CloudFormation |
| `cdk_diff` | Ver diferencias entre local y deployed |
| `cdk_deploy` | Desplegar stack |

---

## 4. AWS Cost Analysis MCP

```json
{
  "mcpServers": {
    "aws-cost": {
      "command": "uvx",
      "args": ["awslabs.cost-analysis-mcp-server@latest"],
      "env": {
        "AWS_PROFILE": "mi-perfil"
      }
    }
  }
}
```

### Para qué sirve

- Análisis de costos por servicio
- Predicciones de gasto
- Recomendaciones de optimización
- Comparativas históricas

### Práctica Guiada

```
Paso 1: Configura el AWS Cost Analysis MCP
Paso 2: "¿Cuál ha sido mi gasto en S3 los últimos 3 meses?"
Paso 3: "¿Qué servicio me está costando más?"
Paso 4: "¿Hay recursos que podría optimizar?"
```

---

## Verificar credenciales

```bash
# Verificar identidad AWS
aws sts get-caller-identity

# Listar perfiles disponibles
aws configure list-profiles
```

---

## 📍 Checkpoint

Verifica que puedes:
- [ ] Ejecutar `aws sts get-caller-identity` correctamente
- [ ] Configurar el MCP con `READ_OPERATIONS_ONLY=true`
- [ ] Listar recursos AWS desde Claude (buckets, instancias, etc.)
- [ ] Entender la diferencia entre los 4 MCPs de AWS

---

## Resumen

| Aspecto | AWS MCPs |
|---------|----------|
| **Mejor para** | Gestión de infraestructura cloud compleja |
| **Precaución** | Siempre usar permisos mínimos y modo solo lectura inicialmente |
| **MCPs disponibles** | API, Knowledge, CDK, Cost Analysis |
| **Requisito** | AWS CLI configurado con perfil IAM limitado |

---

## Recursos

- [AWS MCP Servers](https://github.com/awslabs/mcp)
- [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
