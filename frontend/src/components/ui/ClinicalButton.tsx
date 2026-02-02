import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const clinicalButtonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap font-display font-medium transition-all duration-hover ease-cinematic focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0",
  {
    variants: {
      variant: {
        default:
          "bg-primary text-primary-foreground border border-border hover:bg-primary/80 hover:shadow-clinical-hover",
        cta:
          "bg-cta text-cta-foreground hover:bg-cta/90 shadow-glow-sm hover:shadow-glow-md",
        glow:
          "bg-glow text-glow-foreground hover:bg-glow/90 shadow-glow-md hover:shadow-glow-lg",
        outline:
          "border border-border bg-transparent text-foreground hover:bg-surface hover:border-glow/50",
        ghost:
          "bg-transparent text-foreground hover:bg-surface hover:text-glow",
        link:
          "text-glow underline-offset-4 hover:underline bg-transparent",
      },
      size: {
        default: "h-12 px-6 py-3 text-sm rounded-lg",
        sm: "h-10 px-4 py-2 text-sm rounded-md",
        lg: "h-14 px-8 py-4 text-base rounded-xl",
        xl: "h-16 px-10 py-5 text-lg rounded-xl",
        icon: "h-12 w-12 rounded-lg",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

export interface ClinicalButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof clinicalButtonVariants> {}

const ClinicalButton = React.forwardRef<HTMLButtonElement, ClinicalButtonProps>(
  ({ className, variant, size, ...props }, ref) => {
    return (
      <button
        className={cn(clinicalButtonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    );
  }
);
ClinicalButton.displayName = "ClinicalButton";

export { ClinicalButton, clinicalButtonVariants };
