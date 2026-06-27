export interface User {
  id: number;
  email: string;
  display_name: string;
  created_at: string; // ISO 8601
}

export interface UserCreate {
  email: string;
  password: string;
  display_name: string;
}