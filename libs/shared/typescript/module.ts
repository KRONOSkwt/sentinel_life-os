export interface Module {
  id: number;
  name: string;
  description: string;
  enabled: boolean;
  created_at: string;
}

export interface ModuleCreate {
  name: string;
  description: string;
}