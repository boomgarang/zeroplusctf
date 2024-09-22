import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "./CookieConsent.css";

function CookieConsent() {
  const [isConsentGiven, setIsConsentGiven] = useState<boolean>(false);

  // Проверяем в localStorage, давал ли пользователь согласие
  useEffect(() => {
    const consent = localStorage.getItem("cookieConsent");
    if (consent === "true") {
      setIsConsentGiven(true);
    }
  }, []);

  // Функция для обработки согласия пользователя
  const handleConsent = () => {
    localStorage.setItem("cookieConsent", "true");
    setIsConsentGiven(true);
  };

  // Если согласие уже дано, не показываем баннер
  if (isConsentGiven) {
    return null;
  }

  // Возвращаем баннер, если согласие еще не дано
  return (
    <div className="cookie-consent">
      <p>
        Мы используем cookies для улучшения вашего опыта. Узнайте больше в{" "}
        <Link to="/cookies-dogovor">нашем договоре о cookies</Link>.
      </p>
      <button onClick={handleConsent}>Согласен</button>
    </div>
  );
}

export default CookieConsent;
