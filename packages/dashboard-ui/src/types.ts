export interface Issue {
  id: string;
  slug: string;
  type: 'feat' | 'bug' | 'debt' | 'task' | 'docs';
  title?: string;
  status: 'open' | 'in-progress' | 'blocked' | 'done';
  priority: 'critical' | 'high' | 'medium' | 'low';
  created?: string;
  updated?: string;
  completed?: string;
  agent?: string;
  tags: string[];
  milestone?: string;
  blocked_by: string[];
  related: string[];
  parent?: string;
  body?: string;
  file_path?: string;
}

export interface Milestone {
  id: string;
  slug: string;
  title: string;
  status: 'open' | 'in-progress' | 'completed';
  due_date?: string;
  created?: string;
  target_issues: string[];
  progress_pct: number;
  body?: string;
  file_path?: string;
}

export interface Risk {
  id: string;
  slug: string;
  title: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  status: 'active' | 'mitigated' | 'resolved';
  owner?: string;
  mitigation?: string;
  created?: string;
  updated?: string;
  body?: string;
  file_path?: string;
}

export interface Spike {
  id: string;
  slug: string;
  title: string;
  status: 'hypothesis' | 'evaluating' | 'concluded';
  hypothesis?: string;
  outcome?: string;
  resulting_adr?: string;
  created?: string;
  body?: string;
  file_path?: string;
}

export interface Session {
  id: string;
  slug: string;
  date: string;
  summary: string;
  agent?: string;
  branch?: string;
  commit?: string;
  issues_advanced: string[];
  issues_completed: string[];
  decisions: string[];
  body?: string;
  file_path?: string;
}

export interface Decision {
  id: string;
  number: number;
  slug: string;
  title: string;
  date: string;
  status: string;
  summary: string;
  raw_markdown?: string;
  file_path?: string;
}

export interface KBArticle {
  id: string;
  slug: string;
  title: string;
  type: string;
  tags: string[];
  created?: string;
  updated?: string;
  body?: string;
  file_path?: string;
  incoming_links: string[];
  outgoing_links: string[];
}

export interface DashboardMetrics {
  total_issues: number;
  done_issues: number;
  in_progress_issues: number;
  open_issues: number;
  blocked_issues: number;
  completion_pct: number;
  active_milestones: number;
  active_risks: number;
  total_kb_articles: number;
  total_decisions: number;
  total_sessions: number;
  scan_timestamp: string;
  by_type: Record<string, number>;
  by_priority: Record<string, number>;
}

export interface FullDashboardData {
  repo_name: string;
  agents_dir?: string;
  metrics: DashboardMetrics;
  issues: Issue[];
  milestones: Milestone[];
  risks: Risk[];
  spikes: Spike[];
  sessions: Session[];
  decisions: Decision[];
  kb_articles: KBArticle[];
  graph?: any;
}

export interface SearchResultItem {
  id: string;
  title: string;
  type: string;
  snippet: string;
  score: number;
  url?: string;
  file_path?: string;
}

export interface SearchResponse {
  query: string;
  total: number;
  results: SearchResultItem[];
}
