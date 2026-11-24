
interface ScoreIndicatorProps {
  score: number;
  size?: "sm" | "md" | "lg";
  showBar?: boolean;
}

export const ScoreIndicator: React.FC<ScoreIndicatorProps> = ({
  score,
  size = "md",
  showBar = true,
}) => {
  const safeScore = Math.max(0, Math.min(5, score));
  const percentage = (safeScore / 5) * 100;

  const textSize = {
    sm: "text-xs",
    md: "text-sm",
    lg: "text-lg",
  };

  const color =
    safeScore >= 4
      ? "text-green-600"
      : safeScore >= 2.5
      ? "text-yellow-600"
      : "text-red-600";

  return (
    <div className="flex flex-col gap-1">
      <span className={`font-semibold ${textSize[size]} ${color}`}>
        {safeScore.toFixed(1)} / 5
      </span>

      {showBar && (
        <div className="h-2 w-full rounded-full bg-gray-200">
          <div
            className="h-2 rounded-full bg-blue-600"
            style={{ width: `${percentage}%` }}
          />
        </div>
      )}
    </div>
  );
};
