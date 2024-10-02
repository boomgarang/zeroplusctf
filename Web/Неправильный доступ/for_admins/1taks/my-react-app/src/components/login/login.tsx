import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom"; // Импортируем хук для навигации
import "./Login.css";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate(); // Создаем функцию для перенаправления

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        import.meta.env.VITE_BACKEND_URL + "/api/login",

        {
          email,
          password,
        },
        {
          withCredentials: true, // Этот параметр включает отправку cookies, если это необходимо
        }
      );

      console.log("Response:", response.data); // Лог успешного ответа

      // Если запрос успешен, перенаправляем пользователя на /panel
      navigate("/panel");
    } catch (err: any) {
      console.error("Error:", err);
      setError("Ошибка при входе. Проверьте данные.");
    }
  };

  return (
    <div>
      <h1>Админ панель</h1>
      {error && <p className="error">{error}</p>} {/* Сообщение об ошибке */}
      <form className="form" onSubmit={handleSubmit}>
        <input
          placeholder="Enter your email"
          className="input"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          placeholder="*********"
          className="input"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default Login;
