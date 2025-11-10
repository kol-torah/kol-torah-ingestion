// Type definitions for the API
export interface Rabbi {
  id: number;
  name_hebrew: string;
  name_english: string;
  slug: string;
  website_url?: string;
  created_at: string;
  updated_at: string;
}

export interface RabbiCreate {
  name_hebrew: string;
  name_english: string;
  slug: string;
  website_url?: string;
}

export interface RabbiUpdate {
  name_hebrew?: string;
  name_english?: string;
  slug?: string;
  website_url?: string;
}

export interface Series {
  id: number;
  rabbi_id: number;
  name_hebrew: string;
  name_english: string;
  slug: string;
  description_hebrew?: string;
  description_english?: string;
  website_url?: string;
  type: string;
  created_at: string;
  updated_at: string;
}

export interface SeriesCreate {
  rabbi_id: number;
  name_hebrew: string;
  name_english: string;
  slug: string;
  description_hebrew?: string;
  description_english?: string;
  website_url?: string;
  type: string;
}

export interface SeriesUpdate {
  rabbi_id?: number;
  name_hebrew?: string;
  name_english?: string;
  slug?: string;
  description_hebrew?: string;
  description_english?: string;
  website_url?: string;
  type?: string;
}
