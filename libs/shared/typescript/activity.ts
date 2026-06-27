export interface Activity {
  id: number;
  module_id: number;
  type: string;
  value: number;
  metadata?: Record<string, any>;
  created_at: string;
}

export interface ActivityCreate {
  module_id: number;
  type: string;
  value: number;
  metadata?: Record<string, any>;
}