import React, { createContext, useContext, useEffect, useState } from "react";
import { decodeJwtPayload } from "../utils/auth";

export interface UserProfile {
  id?: number;
  first_name?: string;
  last_name?: string;
  email?: string;
  username?: string;
  modules?: string[];
  permissions?: string[];
}

interface AuthContextValue {
  user: UserProfile | null;
  accessToken: string | null;
  currentModule: string | null;
  setUserFromMe: (me: UserProfile, access?: string, module?: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [user, setUser] = useState<UserProfile | null>(() => {
    try {
      const raw = localStorage.getItem("userProfile");
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  });

  const [accessToken, setAccessToken] = useState<string | null>(() =>
    localStorage.getItem("access"),
  );

  const [currentModule, setCurrentModule] = useState<string | null>(() =>
    localStorage.getItem("currentModule"),
  );

  useEffect(() => {
    if (user) localStorage.setItem("userProfile", JSON.stringify(user));
    else localStorage.removeItem("userProfile");
  }, [user]);

  useEffect(() => {
    if (accessToken) localStorage.setItem("access", accessToken);
  }, [accessToken]);

  useEffect(() => {
    if (currentModule) localStorage.setItem("currentModule", currentModule);
  }, [currentModule]);

  const setUserFromMe = (me: UserProfile, access?: string, module?: string) => {
    setUser(me);
    if (access) setAccessToken(access);
    if (module) setCurrentModule(module);
    // also set roles derived from token if available
    const token = access || accessToken;
    if (token) {
      const claims = decodeJwtPayload(token);
      if (claims?.roles || claims?.role) {
        const roles = claims.roles ?? claims.role;
        localStorage.setItem("userRoles", JSON.stringify(roles));
      }
    }
    localStorage.setItem("loginSuccess", "true");
  };

  const logout = () => {
    setUser(null);
    setAccessToken(null);
    setCurrentModule(null);
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("loginSuccess");
    localStorage.removeItem("userProfile");
    localStorage.removeItem("userRoles");
    localStorage.removeItem("currentModule");
  };

  return (
    <AuthContext.Provider
      value={{ user, accessToken, currentModule, setUserFromMe, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextValue => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
};

export default AuthContext;
