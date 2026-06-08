import React, { useState, useEffect } from 'react';
import WebApp from '@twa-dev/sdk';
import './App.css';

function App() {
  const [language, setLanguage] = useState('ru');
  const [selectedCity, setSelectedCity] = useState('');
  const [selectedPrice, setSelectedPrice] = useState('');
  const [selectedRooms, setSelectedRooms] = useState('');
  const [housings, setHousings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState(null);

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
      loading: '⏳ Загрузка...',
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
      loading: '⏳ Loading...',
      month: '/mo',
      sqm: 'm²',
      hello: 'Hello',
    }
  };

  const t = texts[language];

  // 🔌 ПОДКЛЮЧЕНИЕ К TELEGRAM
  useEffect(() => {
    WebApp.ready();
    WebApp.expand();
    if (WebApp.initDataUnsafe?.user) {
      setUser(WebApp.initDataUnsafe.user);
      const lang = WebApp.initDataUnsafe.user.language_code;
      if (lang === 'ru') setLanguage('ru');
      else setLanguage('en');
    }
  }, []);

  // 📡 ЗАГРУЗКА ДАННЫХ ИЗ API
  useEffect(() => {
    const fetchListings = async () => {
      try {
        setLoading(true);
        const response = await fetch('http://localhost:8000/listings/public');
        const data = await response.json();
        setHousings(data);
      } catch (error) {
        console.error('Ошибка загрузки:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchListings();
  }, []);

  // 🔍 ФИЛЬТРАЦИЯ
  const filtered = housings.filter(h => {
    if (selectedCity && h.city !== selectedCity) return false;
    if (selectedPrice && h.price > parseInt(selectedPrice)) return false;
    if (selectedRooms && h.rooms !== parseInt(selectedRooms)) return false;
    return true;
  });

  const handleContact = (phone, name) => {
    if (WebApp.initDataUnsafe?.user) {
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
        {loading ? (
          <p className="empty">{t.loading}</p>
        ) : filtered.length === 0 ? (
          <p className="empty">{t.noResults}</p>
        ) : (
          filtered.map(h => (
            <div key={h.id} className="card">
<img
  src={h.photos && h.photos.length > 0
    ? h.photos[0].url
    : 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=600&h=400&fit=crop'}
  alt={h.title}
  className="card-img"
/>              <div className="card-body">
                <h2>{h.title}</h2>
                <div className="card-price">${h.price}<span>{t.month}</span></div>
                <div className="card-details">
                  <span>📍 {h.district || h.city}</span>
                  {h.rooms && <span>🛏 {h.rooms}</span>}
                  {h.square && <span>📐 {h.square}{t.sqm}</span>}
                </div>
                <p className="card-desc">{h.description}</p>
                <div className="card-actions">
                  <button
                    className="btn-contact"
                    onClick={() => handleContact(h.phone, h.title)}
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