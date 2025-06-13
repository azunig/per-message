use actix_web::{web, App, HttpResponse, HttpServer, Responder, get, post};
use serde::{Serialize, Deserialize};
use sqlx::mysql::{MySqlPool, MySqlPoolOptions};
use std::env;
use chrono::{DateTime, Utc};
use std::collections::HashMap;

// --- ESTRUCTURAS DE DATOS ---

// Struct #1: Reflejo EXACTO de la tabla de la base de datos.
// Lo usaremos solo para leer los datos con sqlx.
#[derive(sqlx::FromRow, Clone)]
struct MessageFromDb {
    id: u64,
    parent_id: Option<u64>,
    process_id: u64,
    #[sqlx(rename = "type")]
    type_field: String,
    message: String,
    attachment_url: Option<String>,
    is_deleted: i8, // Leemos el booleano como un número (TINYINT -> i8)
    created_at: DateTime<Utc>,
}

// Struct #2: La estructura final que enviaremos como JSON.
// Esta sí tiene 'children' y el booleano correcto.
#[derive(Serialize, Clone)]
struct Message {
    id: u64,
    parent_id: Option<u64>,
    process_id: u64,
    #[serde(rename = "type")]
    type_field: String,
    message: String,
    attachment_url: Option<String>,
    is_deleted: bool, // El tipo correcto para el JSON
    created_at: DateTime<Utc>,
    #[serde(skip_serializing_if = "Vec::is_empty")]
    children: Vec<Message>,
}

// Struct para recibir los datos al crear un mensaje (sin cambios)
#[derive(Deserialize)]
struct CreateMessage {
    parent_id: Option<u64>,
    process_id: u64,
    #[serde(rename = "type")]
    type_field: String,
    message: String,
    attachment_url: Option<String>,
}

// --- MANEJADORES DE RUTAS (CONTROLADORES) ---

#[post("/api/messages")]
async fn create_message(
    pool: web::Data<MySqlPool>,
    new_message: web::Json<CreateMessage>,
) -> impl Responder {
    let insert_result = sqlx::query(
        "INSERT INTO messages (parent_id, process_id, `type`, message, attachment_url) VALUES (?, ?, ?, ?, ?)"
    )
    .bind(new_message.parent_id)
    .bind(new_message.process_id.clone())
    .bind(new_message.type_field.clone())
    .bind(new_message.message.clone())
    .bind(new_message.attachment_url.clone())
    .execute(pool.get_ref())
    .await;

    let last_id = match insert_result {
        Ok(res) => res.last_insert_id(),
        Err(e) => return HttpResponse::InternalServerError().body(format!("Error al crear el mensaje: {}", e)),
    };

    // Leemos el resultado en nuestro struct simple `MessageFromDb`
    match sqlx::query_as::<_, MessageFromDb>(
        "SELECT * FROM messages WHERE id = ?"
    )
    .bind(last_id)
    .fetch_one(pool.get_ref())
    .await
    {
        Ok(db_message) => {
            // Convertimos el struct de la BD al struct final para el JSON
            let final_message = Message {
                id: db_message.id,
                parent_id: db_message.parent_id,
                process_id: db_message.process_id,
                type_field: db_message.type_field,
                message: db_message.message,
                attachment_url: db_message.attachment_url,
                is_deleted: db_message.is_deleted != 0, // Convertimos i8 a bool
                created_at: db_message.created_at,
                children: vec![], // Los hijos siempre están vacíos al crear
            };
            HttpResponse::Created().json(final_message)
        },
        Err(_) => HttpResponse::InternalServerError().body("No se pudo recuperar el mensaje creado."),
    }
}

#[get("/api/processes/{process_id}/thread")]
async fn get_thread_for_process(
    pool: web::Data<MySqlPool>,
    path: web::Path<u64>,
) -> impl Responder {
    let process_id = path.into_inner();

    // Leemos el resultado en un vector de nuestro struct simple `MessageFromDb`
    let messages_from_db = match sqlx::query_as::<_, MessageFromDb>(
        "SELECT * FROM messages WHERE process_id = ? ORDER BY created_at ASC"
    )
    .bind(process_id)
    .fetch_all(pool.get_ref())
    .await
    {
        Ok(messages) => messages,
        Err(_) => return HttpResponse::NotFound().body("No se encontraron mensajes para este proceso."),
    };

    // Convertimos la lista de structs de BD a nuestra lista de structs finales
    let messages: Vec<Message> = messages_from_db.into_iter().map(|db_msg| {
        Message {
            id: db_msg.id,
            parent_id: db_msg.parent_id,
            process_id: db_msg.process_id,
            type_field: db_msg.type_field,
            message: db_msg.message,
            attachment_url: db_msg.attachment_url,
            is_deleted: db_msg.is_deleted != 0, // Convertimos i8 a bool
            created_at: db_msg.created_at,
            children: vec![], // Inicializamos los hijos como un vector vacío
        }
    }).collect();
    
    // La lógica para construir el árbol no cambia
    let mut tree = Vec::new();
    let mut map: HashMap<u64, Message> = messages
        .into_iter()
        .map(|msg| (msg.id, msg))
        .collect();
    
    let keys: Vec<u64> = map.keys().cloned().collect();

    for id in keys {
        if let Some(message) = map.remove(&id) {
            if let Some(parent_id) = message.parent_id {
                if let Some(parent) = map.get_mut(&parent_id) {
                    parent.children.push(message);
                } else {
                    tree.push(message);
                }
            } else {
                tree.push(message);
            }
        }
    }
    HttpResponse::Ok().json(tree)
}


// --- FUNCIÓN PRINCIPAL (Sin cambios) ---
#[actix_web::main]
async fn main() -> std::io::Result<()> {
    dotenvy::dotenv().ok();
    println!("✓ Variables de entorno cargadas");

    let database_url = env::var("DATABASE_URL").expect("DATABASE_URL debe estar definida en .env");
    let pool = MySqlPoolOptions::new()
        .max_connections(5)
        .connect(&database_url)
        .await
        .expect("No se pudo conectar a la base de datos.");
    println!("✓ Conexión a la base de datos establecida");
    
    let port = env::var("PORT").unwrap_or_else(|_| "8001".to_string());
    let port: u16 = port.parse().expect("El puerto debe ser un número válido");
    let address = "127.0.0.1";

    println!("🚀 Servidor iniciado en http://{}:{}", address, port);

    HttpServer::new(move || {
        App::new()
            .app_data(web::Data::new(pool.clone()))
            .service(create_message)
            .service(get_thread_for_process)
    })
    .bind((address, port))?
    .run()
    .await
}