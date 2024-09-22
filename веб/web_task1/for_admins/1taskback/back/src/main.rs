// main.rs
#[macro_use]
extern crate rocket;

use dotenv::dotenv;
use rocket::fairing::{Fairing, Info, Kind};
use rocket::http::{Cookie, CookieJar, Header, Method, Status};
use rocket::response::status::Unauthorized;
use rocket::serde::json::Json;
use rocket::serde::{Deserialize, Serialize};
use rocket::{Request, Response, Rocket};
use std::env;

/// Модель данных для запроса логина
#[derive(Deserialize)]
struct LoginRequest {
    email: String,
    password: String,
}

#[derive(Serialize, Deserialize, Debug)]
struct User {
    email: String,
    password: String,
    role: String,
}

/// Структура для ответа аутентификации
#[derive(Serialize)]
struct AuthResponse {
    authenticated: bool,
    available: bool,
}

/// Структура для логов
#[derive(Serialize)]
struct LogEntry {
    timestamp: String,
    level: String,
    message: String,
}

#[derive(Serialize)]
struct LogsResponse {
    logs: Vec<LogEntry>,
}

/// Структура CORS с разрешёнными доменами
pub struct CORS {
    allowed_origins: Vec<String>,
}

impl CORS {
    /// Создаёт новый экземпляр CORS, загружая разрешённые домены из переменной окружения
    pub fn new() -> Self {
        // Загрузить переменные окружения из .env файла
        dotenv().ok();

        // Получить строку разрешённых доменов из переменной окружения
        let origins = env::var("CORS_ALLOWED_ORIGINS").unwrap_or_else(|_| "*".to_string());

        // Разделить строку по запятым и собрать в вектор
        let allowed_origins = origins
            .split(',')
            .map(|s| s.trim().to_string())
            .collect();

        CORS { allowed_origins }
    }

    /// Проверяет, разрешён ли данный Origin
    fn is_origin_allowed(&self, origin: &str) -> bool {
        self.allowed_origins.contains(&origin.to_string()) || self.allowed_origins.contains(&"*".to_string())
    }
}

#[rocket::async_trait]
impl Fairing for CORS {
    fn info(&self) -> Info {
        Info {
            name: "Add CORS headers to responses",
            kind: Kind::Response,
        }
    }

    /// Добавляет CORS заголовки к каждому ответу
    async fn on_response<'r>(&self, request: &'r Request<'_>, response: &mut Response<'r>) {
        // Получить заголовок Origin из запроса
        if let Some(origin) = request.headers().get_one("Origin") {
            // Проверить, разрешён ли Origin
            if self.is_origin_allowed(origin) {
                response.set_header(Header::new("Access-Control-Allow-Origin", origin));
                response.set_header(Header::new("Access-Control-Allow-Credentials", "true"));
            }
        }

        // Установить общие CORS заголовки
        response.set_header(Header::new(
            "Access-Control-Allow-Methods",
            "POST, GET, OPTIONS, PUT, DELETE",
        ));
        response.set_header(Header::new(
            "Access-Control-Allow-Headers",
            "Content-Type, Authorization",
        ));

        // Если это предзапрос (OPTIONS), установить дополнительные заголовки и статус
        if request.method() == Method::Options {
            response.set_header(Header::new("Access-Control-Max-Age", "86400")); // 1 день
            response.set_status(Status::Ok);
        }
    }
}

/// Маршрут для обработки POST запроса логина
#[post("/login", format = "application/json", data = "<login_data>")]
async fn login(
    login_data: Json<LoginRequest>,
    cookies: &CookieJar<'_>,
) -> Result<String, Unauthorized<String>> {
    // Здесь должна быть асинхронная логика проверки пользователя, например, запрос к базе данных
    // Для примера используем хардкод

    if login_data.email == "User@admin.ru" && login_data.password == "userPassAdmin" {
        // Пользователь найден
        println!("Добро пожаловать, {}!", login_data.email);
        // Устанавливаем куки с ролью пользователя, например, "admin"
        cookies.add(Cookie::new("role", "admin"));
        Ok(format!("Добро пожаловать, {}!", login_data.email))
    } else {
        // Пользователь не найден или неверные учетные данные
        println!("Пользователь не найден или неверный пароль");
        Err(Unauthorized("Неверный логин или пароль".to_string()))
    }
}

/// Маршрут для проверки аутентификации
#[get("/auth")]
async fn auth(cookies: &CookieJar<'_>) -> Result<Json<AuthResponse>, Unauthorized<&'static str>> {
    if let Some(role_cookie) = cookies.get("role") {
        // Если куки "role" существует, проверяем значение куки
        let is_admin = role_cookie.value() == "admin";

        // Возвращаем JSON с полями authenticated и available
        Ok(Json(AuthResponse {
            authenticated: true,
            available: is_admin, // Если роль "admin", то true, иначе false
        }))
    } else {
        // Если куки "role" не существует, возвращаем 401 Unauthorized
        println!("No role cookie found");
        Err(Unauthorized("Unauthorized: No role cookie"))
    }
}

/// Маршрут для получения логов (доступен только админам)
#[get("/logs")]
async fn logs(cookies: &CookieJar<'_>) -> Result<Json<LogsResponse>, Unauthorized<&'static str>> {
    if let Some(role_cookie) = cookies.get("role") {
        if role_cookie.value() == "admin" {
            // Хардкодированные логи
            let hardcoded_logs = LogsResponse {
                logs: vec![
                    LogEntry {
                        timestamp: "2024-04-01T12:00:00Z".to_string(),
                        level: "INFO".to_string(),
                        message: "Система запущена".to_string(),
                    },
                    LogEntry {
                        timestamp: "2024-04-01T12:05:00Z".to_string(),
                        level: "WARN".to_string(),
                        message: "KpkCTF{cookies_is_c00!!!!!!!!!!!}".to_string(),
                    },
                    LogEntry {
                        timestamp: "2024-04-01T12:10:00Z".to_string(),
                        level: "ERROR".to_string(),
                        message: "Не удалось подключиться к базе данных".to_string(),
                    },
                ],
            };

            println!("Логи успешно отправлены");
            Ok(Json(hardcoded_logs))
        } else {
            // Если роль не admin, доступ запрещен
            println!("Доступ к логам запрещен для роли: {}", role_cookie.value());
            Err(Unauthorized("Unauthorized: Insufficient permissions"))
        }
    } else {
        // Если куки "role" не существует, возвращаем 401 Unauthorized
        println!("No role cookie found");
        Err(Unauthorized("Unauthorized: No role cookie"))
    }
}

/// Маршрут для обработки OPTIONS запроса
#[options("/<_..>")]
async fn all_options() -> &'static str {
    "" // Возвращаем пустой ответ для всех предзапросов
}

#[launch]
async fn rocket() -> Rocket<rocket::Build> {
    // Загрузка переменных окружения
    dotenv().ok();

    rocket::build()
        .attach(CORS::new()) // Подключаем CORS
        .mount(
            "/api",
            routes![login, all_options, auth, logs], // Добавляем маршруты
        )
}
