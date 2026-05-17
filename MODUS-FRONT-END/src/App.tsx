import { HashRouter, Route, Routes } from 'react-router-dom'
import './App.css'
import HomePage from './components/pages/HomePage.tsx'
import LogInPage from './components/pages/LogInPage.tsx'
import HomePageLayout from './components/layouts/HomePageLayout.tsx'

function App() {

  return (
    <>
      <HashRouter>
        <Routes>
          <Route element={<HomePageLayout/>}>
            <Route path="/" element={<HomePage/>} />
          </Route>
          <Route path="/login" element={<LogInPage />} />
        </Routes>
      </HashRouter>
    </>
  )
}

export default App
