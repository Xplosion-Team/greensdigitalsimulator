import { GrainOverlay } from "@/components/ui/GrainOverlay";
import { Header } from "@/components/Header";
import { Hero } from "@/components/Hero";
import { OutcomesStrip } from "@/components/OutcomesStrip";
import { ScrollStory } from "@/components/ScrollStory";
import { TrustSection } from "@/components/TrustSection";
import { CTASection } from "@/components/CTASection";
import { Footer } from "@/components/Footer";
import { BrainQuery } from "@/components/BrainQuery";

const Index = () => {
  return (
    <div className="relative min-h-screen bg-background">
      {/* Grain and vignette overlays */}
      <GrainOverlay />

      {/* Navigation */}
      <Header />

      {/* Main content */}
      <main>
        {/* Hero Section */}
        <Hero />

        {/* Outcomes Strip */}
        <OutcomesStrip />

        {/* Scroll Story - GSAP Pinned */}
        <ScrollStory />

        {/* Trust / Explainability Section */}
        <TrustSection />

        {/* Brain Interaction Loop */}
        <BrainQuery />

        {/* Final CTA */}
        <CTASection />
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
};

export default Index;
