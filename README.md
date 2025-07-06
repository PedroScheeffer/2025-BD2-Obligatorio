Proyecto para base de datos II, equipo 3


# Como ejecutar.
Defina el archivo `.env` con los valores de entorno de la base de datos:

```
DB_HOST=***
DB_PORT=***
DB_USER=***
DB_PASSWORD=***
DB_NAME=IC_Grupo3
```

Después, en la consola, en el directorio principal, utilice el comando:

```
docker compose up -d
```

Luego se puede usar las credenciales 
- Funcionario
JKL 004 
contra 1234
- Votante
ABC 001
contra 1234

# Definición de servicios backend

## Servicio Persona
Permite gestionar las personas y sus diferentes roles en el sistema electoral.

### Funcionalidades:
- Registro de ciudadanos con datos personales y circuito electoral asignado
- Gestión de roles: Votante, Presidente de Mesa, Secretario, Vocal, Policía
- Autenticación y autorización de usuarios
- Validación de identidad de votantes
- Control de que cada ciudadano vote solo una vez por elección

### Restricciones:
- Un ciudadano solo puede votar en su circuito asignado
- Votos fuera del circuito asignado se marcan como "observados"
- Votos observados requieren autorización del presidente de mesa
- Mantener anonimato del voto (no se registra a quién votó cada ciudadano)
- No permite múltiples votos por persona en la misma elección

## Servicio Geográfico
Permite gestionar los diferentes modelos de ubicación electoral.

### Funcionalidades:
- Gestión de departamentos, municipios y circuitos electorales
- Asignación de establecimientos y mesas por circuito
- Control de ubicación de votantes
- Generación de estadísticas por ubicación geográfica

### Restricciones:
- Cada circuito debe tener al menos una mesa habilitada
- Los circuitos no pueden modificarse durante el período electoral
- Validación de correspondencia entre votante y circuito

## Servicio Mesa
Controla el funcionamiento de las mesas electorales.

### Funcionalidades:
- Apertura de mesas por circuito
- Control de votación durante horario electoral
- Cierre definitivo de mesas
- Conteo y totalización de votos por mesa
- Generación de actas de escrutinio
- Validación de votos observados por presidente de mesa

### Restricciones:
- **Control estricto de cierre**: Una vez cerrada, no se permite reabrir
- No se permiten más votos después del cierre
- Solo el presidente puede autorizar votos observados
- Los resultados solo son visibles después del cierre de la mesa
- Incremento automático del contador de votos emitidos (sin identificar votante)

## Servicio Elección
Gestiona las diferentes elecciones y procesos de votación.

### Funcionalidades:
- Configuración de elecciones departamentales (Intendente, Ediles, Alcaldes)
- Aplicación de la "Ley de Lemas" para determinar ganadores
- Validación de datos de votación
- Control de períodos electorales
- Gestión de tipos de elección (extensible para futuras elecciones)

### Restricciones:
- Implementación obligatoria de la Ley de Lemas para elecciones departamentales
- El ganador es el candidato más votado del partido más votado
- No se pueden modificar configuraciones durante votación activa
- Validación de integridad de datos electorales

### Ley de Lemas:
- Candidato ganador = candidato más votado del partido más votado
- No necesariamente el candidato con más votos individuales
- Aplicable a elecciones de intendente por departamento

## Servicio Partido
Se encarga de gestionar partidos políticos, listas y candidatos.

### Funcionalidades:
- Registro de partidos políticos
- Gestión de listas electorales por partido
- Registro de candidatos (hasta 3 por partido por departamento para intendente)
- Configuración de candidatos para diferentes cargos:
  - Intendentes por departamento
  - Listas para junta departamental (ediles)
  - Alcaldes por municipio
- Validación de candidaturas

### Restricciones:
- Máximo 3 candidatos a intendente por partido por departamento
- Los candidatos deben estar asociados a un partido registrado
- No se pueden modificar listas durante el período electoral
- Validación de requisitos legales para candidaturas

## Servicio Estadísticas
Nuevo servicio para manejo de reportes y análisis.

### Funcionalidades:
- Generación de estadísticas por circuito
- Estadísticas por departamento
- Estadísticas a nivel nacional
- Reportes de participación electoral
- Análisis de resultados por cargo electoral

### Restricciones:
- Solo accesible después del cierre de mesas
- Datos agregados sin identificación de votantes individuales
- Acceso restringido según roles de usuario

## Flujo de Trabajo del Sistema

### 1. Registro y Autenticación
- El ciudadano se registra en el sistema con sus datos personales
- Se le asigna automáticamente su circuito electoral correspondiente
- Autenticación segura para acceder al sistema de votación

### 2. Proceso de Votación
- **Validación de Circuito**: El sistema verifica que el votante esté en su circuito asignado
- **Voto Normal**: Si coincide el circuito, se registra el voto normalmente
- **Voto Observado**: Si no coincide, se marca como observado y requiere autorización
- **Registro Anónimo**: Se incrementa el contador de votos sin vincular al votante
- **Control de Unicidad**: Se previene que el mismo ciudadano vote múltiples veces

### 3. Gestión de Mesa (Presidente)
- Apertura de mesa al inicio del día electoral
- Autorización de votos observados durante la jornada
- Cierre definitivo de mesa al finalizar el horario
- Acceso a resultados solo después del cierre

### 4. Cálculo de Resultados
- Aplicación automática de la Ley de Lemas
- Determinación de ganadores por departamento
- Generación de estadísticas por nivel geográfico

## Casos de Uso Principales

### CU-01: Votación Ciudadana
**Actor**: Ciudadano
**Precondición**: Mesa abierta, ciudadano registrado
**Flujo**:
1. Ciudadano se autentica en el sistema
2. Sistema valida circuito electoral
3. Si circuito correcto: voto normal
4. Si circuito incorrecto: voto observado (requiere autorización)
5. Sistema registra voto anónimamente
6. Sistema previene votos duplicados

### CU-02: Gestión de Mesa
**Actor**: Presidente de Mesa
**Precondición**: Credenciales de presidente
**Flujo**:
1. Apertura de mesa
2. Supervisión durante votación
3. Autorización de votos observados
4. Cierre definitivo de mesa
5. Acceso a resultados post-cierre

### CU-03: Consulta de Resultados
**Actor**: Presidente de Mesa / Autoridades
**Precondición**: Mesa cerrada
**Flujo**:
1. Verificación de cierre de mesa
2. Cálculo automático con Ley de Lemas
3. Visualización de resultados por cargo
4. Generación de estadísticas

## Reglas de Negocio Críticas

### RN-01: Secreto del Voto
- **Nunca** se debe registrar la relación votante-voto
- Solo se incrementan contadores agregados por opción

### RN-02: Ley de Lemas
- Ganador = candidato más votado del partido más votado
- Se aplica específicamente a elecciones de intendente

### RN-03: Control de Mesa
- Una mesa cerrada **nunca** puede reabrirse
- No se permiten votos después del cierre
- Resultados visibles solo post-cierre

### RN-04: Voto Observado
- Ocurre cuando votante no está en su circuito asignado
- Requiere autorización explícita del presidente
- Se contabiliza por separado inicialmente

### RN-05: Extensibilidad
- El sistema debe soportar futuras elecciones sin reestructuración mayor
- Arquitectura modular para diferentes tipos de cálculo electoral

## Tecnologías y Arquitectura

### Backend
- Python con FastAPI
- Base de datos relacional (MySQL)
- ORM personalizado para manejo de entidades
- Servicios RESTful

### Frontend
- React.js con Vite
- Interfaz responsive para diferentes dispositivos
- Autenticación JWT

### Deployment
- Docker para contenedorización
- Docker Compose para orquestación de servicios