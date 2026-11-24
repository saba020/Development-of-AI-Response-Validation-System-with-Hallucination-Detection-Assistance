
interface LoadingSkeletonProps {
  className?: string;
  rows?: number;
}

export function LoadingSkeleton({
  className = "",
  rows = 1,
}: LoadingSkeletonProps) {
  return (
    <div
      className={`animate-pulse space-y-3 ${className}`}
      aria-label="Loading"
      role="status"
    >
      {Array.from({ length: rows }, (_, index) => (
        <div
          key={index}
          className="h-6 w-full rounded-md bg-gray-200"
        />
      ))}
    </div>
  );
}
