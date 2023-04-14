# Party planner
## Descripción
Es un sistema que se encargará tanto de organizar como de invitar y hacer participe a gente en fiestas, reuniones, etc. Un organizador crea la fiesta, invita a la gente correspondiente y el sistema se encarga de llevar un presupuesto y lista de invitados conforme se vayan aceptando las invitaciones.

## Vistas principales
### Home
En el `Home` se mostrará una bienvenida, un botón para crear fiesta o agregar un código para unirse a una, un widget con las fiestas en las que participa (ya sea organizador o invitado) y (*desire*) un widget con las fiestas cercanas.

### Crear fiesta
En esta vista de `Crear Fiesta` se llenará un form con los datos de la fiesta. Adicionalmente se pondrá un widget de calendario para seleccionar la fecha y hora de la fiesta y otro utilizando la API de Google Maps para seleccionar la ubicación. Se podrá agregar un limite de invitados y un presupuesto, detalles como horario, vestimenta, etc. Finalmente se agregará un botón para guardar la fiesta.

### Vista de invitado
En esta vista de `Detalles` se mostrará la información de la fiesta, quién organiza, widget con la fecha y hora, widget con la ubicación, otro widget con los invitados y uno último de información relevante (vestimenta, horario, etc) y (*desire*) también contendrá un sistema de votación para decidir bebidas, comida, etc, al igual que su estatus de la invitación (pendiente, aceptado, rechazado).

### Vista de organizador
La vista de `Organizador` será la vista más compleja y contendrá la información de la fiesta, fecha y hora, ubicación, widget con la lista de invitados (se puede cambiar por lista de asistentes o poner ambas), un widget con el presupuesto y (*desire*) un widget con las estadísticas de las votaciones. Al igual que un código para que los invitados puedan unirse a la fiesta o bien un link que se pueda compartir.

## Backend
Se utilizará Flask para el backend, aplicando RESTful API mediante JSON. Con esto se podrá crear, editar, eliminar y obtener información de las fiestas, invitados, etc.

### Base de datos
Se utilizará MySQL para la base de datos. La base de datos contendrá las siguientes tablas:
#### Event
| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| id | int | Identificador único |
| name | varchar(255) | Nombre del evento |
| date | datetime | Fecha y hora del evento |
| location | varchar(255) | Ubicación del evento (link) |
| limitGuests | int | Límite de invitados |
| budget | int | id del presupuesto |
| limitBudget | float | Límite del presupuesto |
| organizer | int | Id del organizador |
| description | varchar(255) | Descripción del evento |
| code | varchar(255) | Código para unirse al evento |
| status | boolean | Estado del evento (0: pendiente, 1: finalizado) |

#### User
| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| id | int | Identificador único |
| name | varchar(255) | Nombre del usuario |
| email | varchar(255) | Email del usuario |
| password | varchar(255) | Contraseña del usuario |

#### Guest
| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| id | int | Identificador único |
| user | int | Id del usuario |
| event | int | Id del evento |
| status | int | Estado del invitado (0: pendiente, 1: aceptado, 2: rechazado) |

#### Budget
| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| id | int | Identificador único |
| event | int | Id del evento |
| product | int | Id del producto |
| perperson | float | Presupuesto por persona |
| total | float | Presupuesto total |

#### Product (*desire*)
| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| id | int | Identificador único |
| description | varchar(255) | Nombre del producto |
| price | float | Precio de la comida |
| category | int | Categoria del producto (Posible y posible tabla de categorías) |

#### Vote (*desire*)
| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| id | int | Identificador único |
| event | int | Id del evento |
| product | int | Id del producto |
| user | int | Id del usuario |

#### Details
| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| id | int | Identificador único |
| event | int | Id del evento |
| description | varchar(255) | Descripción del evento |

### Endpoints
Los endpoints que se utilizarán son los siguientes:

### /event
| Método | Endpoint | Descripción | Devuelve |
| :--- | :--- | :--- | :--- |
| `GET` | **/event** | Obtiene todos los eventos | Lista de eventos |
| `GET` | **/event/active** | Obtiene todos los eventos activos | Lista de eventos |
| `GET` | **/event/{id}** | Obtiene un evento específico | Evento |
| `POST` | **/event** | Crea un evento | Evento |
| `PUT` | **/event/{id}** | Edita un evento | Evento |
| `DELETE` | **/event/{id}** | Elimina un evento | Evento |

### /user
| Método | Endpoint | Descripción | Devuelve |
| :--- | :--- | :--- | :--- |
| `GET` | **/user** | Obtiene todos los usuarios | Lista de usuarios |
| `GET` | **/user/{id}** | Obtiene un usuario específico | Usuario |
| `POST` | **/user** | Crea un usuario | Usuario |
| `PUT` | **/user/{id}** | Edita un usuario | Usuario |
| `DELETE` | **/user/{id}** | Elimina un usuario | Usuario |

### /guest
| Método | Endpoint | Descripción | Devuelve |
| :--- | :--- | :--- | :--- |
| `GET` | **/event/{id}/guest** | Obtiene todos los invitados | Lista de invitados |
| `POST` | **/event/{id}/guest** | Crea un invitado en un evento por su id | Invitado |
| `PUT` | **/event/{id}/guest/{id}** | Edita un invitado específico | Invitado |
| `PUT` | **/event/{id}/guest/{id}/accept** | Acepta un invitado específico | Invitado |
| `PUT` | **/event/{id}/guest/{id}/reject** | Rechaza un invitado específico | Invitado |

### /product (*desire*)
| Método | Endpoint | Descripción | Devuelve |
| :--- | :--- | :--- | :--- |
| `GET` | **/product** | Obtiene todos los productos | Lista de productos |
| `GET` | **/product/{id}** | Obtiene un producto específico | Producto |
| `POST` | **/product** | Crea un producto | Producto |
| `PUT` | **/product/{id}/{price}** | Edita el precio de un producto | Producto |

### /budget
| Método | Endpoint | Descripción | Devuelve |
| :--- | :--- | :--- | :--- |
| `GET` | **/event/{id}/budget** | Obtiene el presupuesto de un evento | Presupuesto |
| `PUT` | **/event/{id}/budget/plus/{id_product}* | Aumenta el presupuesto mediante un producto | Presupuesto |
| `PUT` | **/event/{id}/budget/minus/{id_product}* | Disminuye el presupuesto mediante un producto | Presupuesto |

### /vote (*desire*)
| Método | Endpoint | Descripción | Devuelve |
| :--- | :--- | :--- | :--- |
| `GET` | **/event/{id}/vote** | Obtiene todos los votos de un evento | Lista de votos |
| `GET` | **/event/{id}/vote/{category}** | Obtiene todos los votos de un producto por categoría | Lista de votos (Posible) |
| `POST` | **/event/{id}/vote/{id_product}** | Crea un voto en un evento | Voto |
| `PUT` | **/event/{id}/vote/{id_product}** | Edita un voto específico | Voto |


## Frontend
El frontend está pensado para que sea lo más sencillo posible, con un diseño minimalista y una interfaz intuitiva por lo mismo no cuenta con una gran cantidad de vistas, para su practicidad se está pensando en utilizar HTML, CSS y JavaScript combinado con Bootstrap para la rapidez del diseño y funcionalidad.

### Vistas
Las vistas que se utilizarán son las siguientes:
- **Login**: Vista para iniciar sesión.
- **Signup**: Vista para registrarse.
- **Home**: Vista principal, donde se muestran los eventos.
- **Event**: Vista para ver los detalles de un evento.
- **Create**: Vista para crear un evento.
- **Edit**: Vista para editar un evento.
- **Organize**: Vista de organizador, donde se muestran los detalles del evento.


To create the MySQL connection is needed to get the IPV4 and then execute the following mysql:
```sql
SELECT host FROM mysql.user WHERE User = 'root';  -- To get all the IPV4 of the root user
CREATE USER 'root'@'ip_address' IDENTIFIED BY 'pass';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'ip_address';

FLUSH PRIVILEGES;
```