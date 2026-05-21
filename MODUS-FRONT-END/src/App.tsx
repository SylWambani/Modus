import { HashRouter, Route, Routes } from 'react-router-dom'
import './App.css'
import HomePage from './components/pages/HomePage.tsx'
import LogInPage from './components/pages/LogInPage.tsx'
import HomePageLayout from './components/layouts/HomePageLayout.tsx'
import DashBoardPage from './components/pages/DashBoardPage.tsx'

function App() {

  return (
    <>
      <HashRouter>
        <Routes>
          <Route element={<HomePageLayout />}>
            <Route path="/" element={<HomePage />} />
          </Route>
          <Route path="/login" element={<LogInPage />} />
          <Route path="/dashboard" element={<DashBoardPage />} />
        </Routes>
      </HashRouter>
    </>
  );
}

export default App
