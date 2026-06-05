export interface UserClaims {
  email?: string;
  role?: string | string[];
  roles?: string[];
  permissions?: string[];
  scope?: string | string[];
  [key: string]: any;
}

const safeJsonParse = <T>(value: string | null): T | null => {
  if (!value) return null;
  try {
    return JSON.parse(value) as T;
  } catch {
    return null;
  }
};

const normalizeArray = (value: string | string[] | undefined): string[] => {
  if (!value) return [];
  if (Array.isArray(value))
    return value.map((item) => String(item).toLowerCase());
  return String(value)
    .split(/[,\s]+/)
    .map((item) => item.toLowerCase())
    .filter(Boolean);
};

export const decodeJwtPayload = (token: string): UserClaims | null => {
  if (!token) return null;
  const parts = token.split(".");
  if (parts.length < 2) return null;
  try {
    const payload = atob(parts[1].replace(/-/g, "+").replace(/_/g, "/"));
    return JSON.parse(decodeURIComponent(escape(payload)));
  } catch {
    return null;
  }
};

export const getAccessToken = (): string | null =>
  localStorage.getItem("access");

export const isAuthenticated = (): boolean => {
  return Boolean(
    getAccessToken() && localStorage.getItem("loginSuccess") === "true",
  );
};

export const getUserRoles = (): string[] => {
  const storedRoles = safeJsonParse<string[]>(
    localStorage.getItem("userRoles"),
  );
  if (storedRoles && Array.isArray(storedRoles) && storedRoles.length > 0) {
    return storedRoles.map((role) => role.toLowerCase());
  }

  const token = getAccessToken();
  if (!token) return [];

  const claims = decodeJwtPayload(token);
  if (!claims) return [];

  let roles: string[] = [];
  if (claims.roles) {
    roles = normalizeArray(claims.roles);
  } else if (claims.role) {
    roles = normalizeArray(claims.role);
  } else if (claims.permissions) {
    roles = normalizeArray(claims.permissions);
  } else if (claims.scope) {
    roles = normalizeArray(claims.scope);
  }

  if (roles.length > 0) {
    localStorage.setItem("userRoles", JSON.stringify(roles));
  }

  return roles;
};

export const userHasModuleAccess = (module: string): boolean => {
  const roles = getUserRoles();
  if (!roles.length) return false;

  if (module === "procurement") {
    return roles.some((role) =>
      [
        "procurement",
        "procurement_officer",
        "procurement officer",
        "procurement-manager",
        "procurement manager",
      ].includes(role),
    );
  }

  return true;
};
