
export enum GlucoseState {
  Stable = "Stable",
  TrendingHigh = "Trending High",
  High = "High",
  TrendingLow = "Trending Low",
  Low = "Low",
  RapidRise = "Rapid Rise",
  RapidFall = "Rapid Fall"
}

export interface GlucoseReading {
  value: number;
  trend: number; // rate of change in mg/dL per minute
  timestamp: string;
}

export const CLASSIFICATION_THRESHOLDS = {
  LOW: 70,
  HIGH: 180,
  TREND_STABLE: 1,
  TREND_RAPID: 2
};

export function classifyGlucoseState(currentGlucose: number, trend: number): GlucoseState {
  if (currentGlucose < CLASSIFICATION_THRESHOLDS.LOW) return GlucoseState.Low;
  if (currentGlucose > CLASSIFICATION_THRESHOLDS.HIGH) return GlucoseState.High;

  if (trend > CLASSIFICATION_THRESHOLDS.TREND_RAPID) return GlucoseState.RapidRise;
  if (trend > CLASSIFICATION_THRESHOLDS.TREND_STABLE) return GlucoseState.TrendingHigh;
  if (trend < -CLASSIFICATION_THRESHOLDS.TREND_RAPID) return GlucoseState.RapidFall;
  if (trend < -CLASSIFICATION_THRESHOLDS.TREND_STABLE) return GlucoseState.TrendingLow;

  return GlucoseState.Stable;
}
