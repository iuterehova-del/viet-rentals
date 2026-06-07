import React, { useState, useEffect } from 'react';
import WebApp from '@twa-dev/sdk';
import './App.css';

function App() {
  const [language, setLanguage] = useState('ru');
  const [selectedCity, setSelectedCity] = useState('');
  const [selectedPrice, setSelectedPrice] = useState('');
  const [selectedRooms, setSelectedRooms] = useState('');
  const [user, setUser] = useState(null);

  // 🔌 ПОДКЛЮЧЕНИЕ К TELEGRAM
  useEffect(() => {
    WebApp.ready();
    WebApp.expand(); // Разворачиваем на весь экран

    // Получаем данные пользователя из Telegram
    if (WebApp.initDataUnsafe?.user) {
      setUser(WebApp.initDataUnsafe.user);
      // Если язык пользователя русский - ставим РУ
      const lang = WebApp.initDataUnsafe.user.language_code;
      if (lang === 'ru') setLanguage('ru');
      else setLanguage('en');
    }
  }, []);

  const texts = {
    ru: {
      title: '🏠 Аренда жилья во Вьетнаме',
      city: 'Город',
      price: 'Цена в месяц',
      rooms: 'Комнат',
      all: 'Все',
      contact: '📞 Контакт',
      save: '❤️ Сохранить',
      noResults: '😔 Ничего не найдено',
      month: '/мес',
      sqm: 'м²',
      hello: 'Привет',
    },
    en: {
      title: '🏠 Vietnam Rentals',
      city: 'City',
      price: 'Price per month',
      rooms: 'Rooms',
      all: 'All',
      contact: '📞 Contact',
      save: '❤️ Save',
      noResults: '😔 No results found',
      month: '/mo',
      sqm: 'm²',
      hello: 'Hello',
    }
  };

  const t = texts[language];

  const housings = [
    {
      id: 1,
      title: { ru: '1-комнатная у пляжа', en: '1-bedroom near beach' },
      price: 600,
      city: 'Nha Trang',
      district: { ru: 'Центр', en: 'City Center' },
      rooms: 1,
      square: 40,
      phone: '+84912345678',
      description: { ru: 'Уютная квартира с видом на море', en: 'Cozy apartment with sea view' },
      image: 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=500'
    },
    {
      id: 2,
      title: { ru: '2-комнатная с кондиционером', en: '2-bedroom with AC' },
      price: 900,
      city: 'Nha Trang',
      district: { ru: 'Кай Дьеу', en: 'Kai Dieu' },
      rooms: 2,
      square: 65,
      phone: '+84987654321',
      description: { ru: 'Современная квартира, всё включено', en: 'Modern apartment, all inclusive' },
      image: 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=500'
    },
    {
      id: 3,
      title: { ru: '3-комнатная вилла с бассейном', en: '3-bedroom villa with pool' },
      price: 1500,
      city: 'Da Nang',
      district: { ru: 'Пригород', en: 'Suburbs' },
      rooms: 3,
      square: 120,
      phone: '+84911111111',
      description: { ru: 'Просторная вилла, свой бассейн', en: 'Spacious villa with private pool' },
      image: 'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=500'
    },
    {
      id: 4,
      title: { ru: 'Студия эконом класс', en: 'Budget studio' },
      price: 350,
      city: 'Ho Chi Minh',
      district: { ru: 'Район 1', en: 'District 1' },
      rooms: 1,
      square: 28,
      phone: '+84922222222',
      description: { ru: 'Недорогое жилье в центре города', en: 'Affordable housing in city center' },
      image: 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=500'
    },
    {
      id: 5,
      title: { ru: '2-комнатная у моря', en: '2-bedroom sea view' },
      price: 1100,
      city: 'Da Nang',
      district: { ru: 'Пляж Мидан', en: 'My Khe Beach' },
      rooms: 2,
      square: 70,
      phone: '+84933333333',
      description: { ru: 'Вид на море, 5 минут до пляжа', en: 'Sea view, 5 min to beach' },
      image: 'https://images.unsplash.com/photo-1484154218962-a197022b5858?w=500'
    },
  ];

  const filtered = housings.filter(h => {
    if (selectedCity && h.city !== selectedCity) return false;
    if (selectedPrice && h.price > parseInt(selectedPrice)) return false;
    if (selectedRooms && h.rooms !== parseInt(selectedRooms)) return false;
    return true;
  });

  // Показываем popup через Telegram
  const handleContact = (phone, name) => {
    if (WebApp.initDataUnsafe?.user) {
      // Открываем через Telegram
      WebApp.showPopup({
        title: t.contact,
        message: `${name}\n📞 ${phone}`,
        buttons: [
          { id: 'call', type: 'default', text: '📞 Позвонить' },
          { id: 'cancel', type: 'cancel' }
        ]
      }, (buttonId) => {
        if (buttonId === 'call') {
          window.open(`tel:${phone}`);
        }
      });
    } else {
      // В браузере (для теста)
      window.open(`tel:${phone}`);
    }
  };

  const handleSave = () => {
    if (WebApp.initDataUnsafe?.user) {
      WebApp.showAlert('❤️ Сохранено!');
    } else {
      alert('❤️ Сохранено!');
    }
  };

  return (
    <div className="app">
      <header className="header">
        <div className="header-left">
          <h1>{t.title}</h1>
          {user && (
            <p className="user-greeting">
              {t.hello}, {user.first_name}! 👋
            </p>
          )}
        </div>
        <div className="lang-switch">
          <button onClick={() => setLanguage('ru')} className={language === 'ru' ? 'active' : ''}>🇷🇺</button>
          <button onClick={() => setLanguage('en')} className={language === 'en' ? 'active' : ''}>🇬🇧</button>
        </div>
      </header>

      <div className="filters">
        <div className="filter-row">
          <div className="filter-item">
            <label>{t.city}</label>
            <select value={selectedCity} onChange={e => setSelectedCity(e.target.value)}>
              <option value="">{t.all}</option>
              <option value="Nha Trang">Nha Trang</option>
              <option value="Da Nang">Da Nang</option>
              <option value="Ho Chi Minh">Ho Chi Minh</option>
            </select>
          </div>
          <div className="filter-item">
            <label>{t.price}</label>
            <select value={selectedPrice} onChange={e => setSelectedPrice(e.target.value)}>
              <option value="">{t.all}</option>
              <option value="500">до $500</option>
              <option value="1000">до $1000</option>
              <option value="1500">до $1500</option>
              <option value="9999">$1500+</option>
            </select>
          </div>
          <div className="filter-item">
            <label>{t.rooms}</label>
            <select value={selectedRooms} onChange={e => setSelectedRooms(e.target.value)}>
              <option value="">{t.all}</option>
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
            </select>
          </div>
        </div>
      </div>

      <div className="listings">
        {filtered.length === 0 ? (
          <p className="empty">{t.noResults}</p>
        ) : (
          filtered.map(h => (
            <div key={h.id} className="card">
              <img src={h.image} alt={h.title[language]} className="card-img" />
              <div className="card-body">
                <h2>{h.title[language]}</h2>
                <div className="card-price">${h.price}<span>{t.month}</span></div>
                <div className="card-details">
                  <span>📍 {h.district[language]}</span>
                  <span>🛏 {h.rooms}</span>
                  <span>📐 {h.square}{t.sqm}</span>
                </div>
                <p className="card-desc">{h.description[language]}</p>
                <div className="card-actions">
                  <button
                    className="btn-contact"
                    onClick={() => handleContact(h.phone, h.title[language])}
                  >
                    {t.contact}
                  </button>
                  <button className="btn-save" onClick={handleSave}>
                    {t.save}
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default App;