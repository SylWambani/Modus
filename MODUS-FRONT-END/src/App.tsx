import { HashRouter, Route, Routes } from 'react-router-dom'
import './App.css'
import HomePage from './components/pages/HomePage.tsx'
import HomePageLayout from './components/layouts/HomePageLayout.tsx'

function App() {

  return (
    <>
      <HashRouter>
        <Routes>
          <Route element={<HomePageLayout/>}>
            <Route path="/" element={<HomePage/>} />
          </Route>
          
        </Routes>
      </HashRouter>
    </>
  )
}

export default App
