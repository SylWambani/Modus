import { HashRouter, Route, Routes } from "react-router-dom";
import "./App.css";
import HomePage from "./components/pages/HomePage.tsx";
import LogInPage from "./components/pages/LogInPage.tsx";
import HomePageLayout from "./components/layouts/HomePageLayout.tsx";
import ProtectedRoute from "./components/ui/ProtectedRoute.tsx";
import ProcurementLandingPage from "./components/pages/landingpages/ProcurementLandingPage.tsx";
import InventoryLandingPage from "./components/pages/landingpages/InventoryLandingPage.tsx";
import HRLandingPage from "./components/pages/landingpages/HRLandingPage.tsx";
import AccountingLandingPage from "./components/pages/landingpages/AccountingLandingPage.tsx";
import ProcurementDashboard from "./components/pages/dashboardpages/ProcurementDashboard.tsx";

function App() {
  return (
    <>
      <HashRouter>
        <Routes>
          <Route element={<HomePageLayout />}>
            <Route path="/" element={<HomePage />} />
          </Route>
          <Route path="/:module/login" element={<LogInPage />} />
          <Route path="/procurement" element={<ProcurementLandingPage />} />
          <Route path="/inventory" element={<InventoryLandingPage />} />
          <Route path="/hr" element={<HRLandingPage />} />
          <Route path="/accounting" element={<AccountingLandingPage />} />
          <Route
            path="/procurement/dashboard"
            element={
              <ProtectedRoute requiredModule="procurement">
                <ProcurementDashboard />
              </ProtectedRoute>
            }
          />
        </Routes>
      </HashRouter>
    </>
  );
}

export default App;
