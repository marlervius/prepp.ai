export interface BriefSource {
  title: string;
  url: string;
  source: string;
}

export interface BriefContent {
  lk20_kobling: string;
  faglig_dybde: string;
  pedagogiske_tips: string;
  elev_sporsmal_feller: string;
  kilder: string;
}

export interface Brief {
  id: string;
  subject: string;
  grade: string;
  topic: string;
  content: BriefContent;
  sources: BriefSource[];
  processing_time_ms: number;
  created_at: string;
}
