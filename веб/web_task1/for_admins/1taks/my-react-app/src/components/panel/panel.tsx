import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { Bar, Line, Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import "./Panel.css";

// Регистрация всех элементов для графиков
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

// Определение интерфейсов для типизации данных
interface AuthResponse {
  authenticated: boolean;
  available: boolean;
}

interface LogEntry {
  timestamp: string;
  level: string;
  message: string;
}

interface LogsResponse {
  logs: LogEntry[];
}

function Panel() {
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [available, setAvailable] = useState(false);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const navigate = useNavigate();

  // Функция для проверки авторизации
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const authResponse = await axios.get<AuthResponse>(
          import.meta.env.VITE_BACKEND_URL + "/api/auth",
          {
            withCredentials: true,
          }
        );
        if (authResponse.data.authenticated) {
          setIsAuthenticated(true);
          setAvailable(authResponse.data.available);
          console.log("Authentication successful");
        } else {
          navigate("/"); // Перенаправляем на страницу логина
        }
      } catch (error) {
        console.error("Authentication failed:", error);
        navigate("/"); // В случае ошибки также перенаправляем на логин
      } finally {
        setIsLoading(false); // Останавливаем загрузку
      }
    };
    checkAuth();
  }, [navigate]);

  // Получение логов
  useEffect(() => {
    if (isAuthenticated && available) {
      const fetchLogs = async () => {
        try {
          const logsResponse = await axios.get<LogsResponse>(
            import.meta.env.VITE_BACKEND_URL + "/api/logs",
            {
              withCredentials: true,
            }
          );
          setLogs(logsResponse.data.logs);
        } catch (error: any) {
          if (error.response && error.response.status === 401) {
            console.log("Unauthorized access to logs");
            setLogs([]); // Если 401, то оставляем пустое поле логов
          } else {
            console.error("Failed to fetch logs:", error);
          }
        }
      };
      fetchLogs();
    }
  }, [isAuthenticated, available]);

  // Реалистичные данные для графиков

  // Пример данных для графика "Продажи по месяцам"
  const salesData = {
    labels: [
      "Январь",
      "Февраль",
      "Март",
      "Апрель",
      "Май",
      "Июнь",
      "Июль",
      "Август",
      "Сентябрь",
      "Октябрь",
      "Ноябрь",
      "Декабрь",
    ],
    datasets: [
      {
        label: "Продажи (тыс. руб.)",
        data: [50, 65, 80, 70, 90, 100, 95, 85, 110, 120, 130, 125],
        fill: false,
        borderColor: "rgba(75,192,192,1)",
        backgroundColor: "rgba(75,192,192,0.4)",
        tension: 0.1,
      },
    ],
  };

  // Пример данных для графика "Посещаемость сайта"
  const trafficData = {
    labels: [
      "Понедельник",
      "Вторник",
      "Среда",
      "Четверг",
      "Пятница",
      "Суббота",
      "Воскресенье",
    ],
    datasets: [
      {
        label: "Посетители (тыс.)",
        data: [30, 45, 60, 50, 70, 80, 65],
        backgroundColor: "rgba(255, 159, 64, 0.6)",
        borderColor: "rgba(255, 159, 64, 1)",
        borderWidth: 1,
      },
    ],
  };

  // Пример данных для графика "Распределение пользователей по устройствам"
  const userDistributionData = {
    labels: ["Мобильные устройства", "Десктопы", "Планшеты"],
    datasets: [
      {
        label: "Пользователи (%)",
        data: [60, 30, 10],
        backgroundColor: ["#36A2EB", "#FF6384", "#FFCE56"],
        hoverBackgroundColor: ["#36A2EB", "#FF6384", "#FFCE56"],
      },
    ],
  };

  // Лоудер во время загрузки данных
  if (isLoading) {
    return <div>Загрузка...</div>;
  }

  // Если available === false, выводим "НЕТ ДОСТУПА"
  if (!available) {
    return (
      <div className="no-access">
        <h1>НЕТ ДОСТУПА</h1>
      </div>
    );
  }

  // Если авторизация успешна и доступ разрешен (available === true), отображаем графики и логи
  return (
    <div className="panel-container">
      <h1>Панель управления</h1>
      <div className="charts-row">
        <div className="chart-container">
          <h2 className="text">Продажи по месяцам</h2>
          <Line data={salesData} options={{ maintainAspectRatio: false }} />
        </div>
        <div className="chart-container">
          <h2 className="text">Посещаемость сайта</h2>
          <Bar data={trafficData} options={{ maintainAspectRatio: false }} />
        </div>
      </div>

      <div className="charts-row">
        <div className="chart-container">
          <h2 className="text">Распределение пользователей по устройствам</h2>
          <Pie
            data={userDistributionData}
            options={{ maintainAspectRatio: false }}
          />
        </div>

        <div className="logs-container">
          <h2 className="text">Логи</h2>
          {logs.length === 0 ? (
            <p className="text">Нет доступных логов</p>
          ) : (
            <ul>
              {logs.map((log, index) => (
                <li
                  key={index}
                  className={`log-entry ${log.level.toLowerCase()}`}
                >
                  <span className="log-timestamp">
                    {new Date(log.timestamp).toLocaleString()}:
                  </span>
                  <span className={`log-level ${log.level.toLowerCase()}`}>
                    {log.level}
                  </span>
                  <span> </span>
                  <span className="log-message">{log.message}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}

export default Panel;
