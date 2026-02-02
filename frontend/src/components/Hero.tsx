import { motion, type Variants } from "framer-motion";
import { VitalsRibbon } from "@/components/ui/VitalsRibbon";
import { ClinicalButton } from "@/components/ui/ClinicalButton";
import { ArrowRight, Activity } from "lucide-react";

const containerVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.12,
      delayChildren: 0.2,
    },
  },
};

const itemVariants: Variants = {
  hidden: { opacity: 0, y: 30 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.9,
      ease: [0.22, 1, 0.36, 1] as const,
    },
  },
};

const Hero = () => {

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Vitals background animation */}
      <VitalsRibbon className="z-0" />

      {/* Gradient blobs */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="gradient-blob gradient-blob-primary w-[800px] h-[800px] -top-40 -right-40" />
        <div className="gradient-blob gradient-blob-accent w-[600px] h-[600px] bottom-0 -left-40" />
      </div>

      {/* Content */}
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="container-clinical relative z-10 text-center py-20"
      >
        {/* Badge */}
        <motion.div variants={itemVariants} className="mb-8">
          <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/40 border border-border text-sm text-glow font-medium">
            <Activity className="w-4 h-4" />
            Blood Pressure Digital Twin
          </span>
        </motion.div>

        {/* Main heading */}
        <motion.h1
          variants={itemVariants}
          className="font-display text-5xl md:text-6xl lg:text-7xl xl:text-8xl font-bold text-foreground leading-[1.1] tracking-tight mb-6"
        >
          <span className="block">Your heart's future,</span>
          <span className="block text-glow text-glow">predicted today</span>
        </motion.h1>

        {/* Subheading */}
        <motion.p
          variants={itemVariants}
          className="max-w-2xl mx-auto text-lg md:text-xl text-muted-foreground leading-relaxed mb-10"
        >
          Greens Health creates a personalized digital twin of your cardiovascular system—
          understanding patterns, predicting risks, and guiding you toward lasting control.
        </motion.p>

        {/* CTA buttons */}
        <motion.div
          variants={itemVariants}
          className="flex flex-col sm:flex-row items-center justify-center gap-4"
        >
          <ClinicalButton variant="cta" size="lg" className="group">
            Start your journey
            <ArrowRight className="w-5 h-5 transition-transform duration-hover group-hover:translate-x-1" />
          </ClinicalButton>
          <ClinicalButton variant="outline" size="lg">
            Watch demo
          </ClinicalButton>
        </motion.div>

        {/* Trust indicators */}
        <motion.div
          variants={itemVariants}
          className="mt-16 flex items-center justify-center gap-8 text-sm text-muted-foreground"
        >
          <span className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-glow animate-pulse-glow" />
            HIPAA Compliant
          </span>
          <span className="hidden sm:block w-px h-4 bg-border" />
          <span className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-glow animate-pulse-glow" />
            SOC 2 Type II
          </span>
          <span className="hidden sm:block w-px h-4 bg-border" />
          <span className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-glow animate-pulse-glow" />
            FDA Registered
          </span>
        </motion.div>
      </motion.div>

      {/* Scroll indicator */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.5, duration: 0.6 }}
        className="absolute bottom-8 left-1/2 -translate-x-1/2"
      >
        <div className="w-6 h-10 rounded-full border-2 border-muted flex items-start justify-center p-2">
          <motion.div
            animate={{ y: [0, 12, 0] }}
            transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
            className="w-1.5 h-1.5 rounded-full bg-glow"
          />
        </div>
      </motion.div>
    </section>
  );
};

export { Hero };
