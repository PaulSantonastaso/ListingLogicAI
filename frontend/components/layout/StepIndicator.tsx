import { cn } from "@/lib/utils";
import { STEP_LABELS, STEP_ORDER, type Step } from "@/types";

interface StepIndicatorProps {
  currentStep: Step;
  showLabels?: boolean;
  className?: string;
}

export function StepIndicator({
  currentStep,
  showLabels = false,
  className,
}: StepIndicatorProps) {
  const currentIndex = STEP_ORDER.indexOf(currentStep);

  return (
    <div className={cn("flex flex-col items-center gap-1", className)}>
      {/* Pips row */}
      <div className="flex items-center gap-0">
        {STEP_ORDER.map((step, index) => {
          const isDone = index < currentIndex;
          const isActive = index === currentIndex;
          const isLast = index === STEP_ORDER.length - 1;

          return (
            <div key={step} className="flex items-center">
              {/* Pip */}
              <div
                aria-label={`Step ${index + 1}: ${STEP_LABELS[step]}${isDone ? " (complete)" : isActive ? " (current)" : ""}`}
                className={cn(
                  "h-2 w-2 rounded-full transition-all duration-200",
                  isDone && "bg-foreground",
                  isActive && "bg-foreground pip-active",
                  !isDone && !isActive && "bg-border"
                )}
              />
              {/* Connector line between pips */}
              {!isLast && (
                <div className="mx-1.5 h-px w-5 bg-border" />
              )}
            </div>
          );
        })}
      </div>

      {/* Optional labels row */}
      {showLabels && (
        <div className="flex items-center gap-0">
          {STEP_ORDER.map((step, index) => {
            const isDone = index < currentIndex;
            const isActive = index === currentStep;
            const isLast = index === STEP_ORDER.length - 1;

            return (
              <div key={step} className="flex items-center">
                <span
                  className={cn(
                    "text-[9px] leading-none",
                    isActive ? "font-semibold text-foreground" : "text-muted-foreground"
                  )}
                >
                  {STEP_LABELS[step]}
                </span>
                {/* Spacer to align labels under connectors */}
                {!isLast && <div className="mx-1.5 w-5" />}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
