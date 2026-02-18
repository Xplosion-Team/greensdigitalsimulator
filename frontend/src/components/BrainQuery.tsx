import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Brain, Send, Loader2, Thermometer, LineChart as ChartIcon, Quote } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { toast } from "sonner";
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    ReferenceLine,
    Area,
    AreaChart
} from "recharts";

interface DataPoint {
    time_mins: number;
    glucose: number;
}

export const BrainQuery = () => {
    const [query, setQuery] = useState("");
    const [glucose, setGlucose] = useState("120");
    const [isLoading, setIsLoading] = useState(false);
    const [response, setResponse] = useState<string | null>(null);
    const [chartData, setChartData] = useState<DataPoint[] | null>(null);

    const handleQuery = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!query.trim()) return;

        setIsLoading(true);
        setResponse(null);

        try {
            const res = await fetch("http://localhost:8000/v1/brain/query", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    text: query,
                    current_glucose: parseFloat(glucose),
                    digital_twin_id: 1,
                }),
            });

            if (!res.ok) {
                throw new Error("Failed to fetch from Brain API");
            }

            const data = await res.json();
            if (data.success) {
                setResponse(data.explanation);
                if (data.simulation_data) {
                    setChartData(data.simulation_data);
                }
            } else {
                toast.error(data.message || "An error occurred with the Brain engine");
            }
        } catch (error) {
            console.error("Brain Query Error:", error);
            toast.error("Could not connect to the Brain API. Is the server running?");
        } finally {
            setIsLoading(false);
        }
    };

    const CustomTooltip = ({ active, payload }: any) => {
        if (active && payload && payload.length) {
            return (
                <div className="bg-background/90 backdrop-blur-sm border border-primary/20 p-3 rounded-lg shadow-xl">
                    <p className="text-xs text-muted-foreground mb-1">{payload[0].payload.time_mins} mins</p>
                    <p className="text-lg font-bold text-primary">
                        {payload[0].value} <span className="text-xs font-normal text-muted-foreground ml-1">mg/dL</span>
                    </p>
                </div>
            );
        }
        return null;
    };

    return (
        <section className="py-24 px-6 relative overflow-hidden" id="brain-interaction">
            {/* Background blobs for premium feel */}
            <div className="absolute top-1/4 -left-20 w-80 h-80 bg-primary/5 rounded-full blur-[100px] pointer-events-none" />
            <div className="absolute bottom-1/4 -right-20 w-80 h-80 bg-primary/5 rounded-full blur-[100px] pointer-events-none" />

            <div className="max-w-5xl mx-auto">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                    viewport={{ once: true }}
                    className="text-center mb-16"
                >
                    <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-primary/5 text-primary text-sm font-semibold mb-6 border border-primary/10 tracking-wide uppercase">
                        <Brain className="w-4 h-4" />
                        <span>Neural Intelligence Layer</span>
                    </div>
                    <h2 className="text-4xl md:text-6xl font-black mb-6 font-serif tracking-tight text-foreground">
                        Ask the <span className="text-primary italic">Brain</span>
                    </h2>
                    <p className="text-muted-foreground text-xl max-w-2xl mx-auto font-light leading-relaxed">
                        Predict outcomes and receive clinical-grade AI summaries in seconds.
                    </p>
                </motion.div>

                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
                    {/* Controls Panel */}
                    <Card className="lg:col-span-4 glass border-primary/5 shadow-2xl overflow-hidden self-start">
                        <CardHeader className="space-y-1">
                            <CardTitle className="text-xl flex items-center gap-2">
                                <Brain className="w-5 h-5 text-primary" />
                                Scenario Input
                            </CardTitle>
                            <CardDescription>
                                Define your next meal or activity.
                            </CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-6 pt-2">
                            <form onSubmit={handleQuery} className="space-y-6">
                                <div className="space-y-4">
                                    <div className="space-y-2">
                                        <Label htmlFor="query" className="text-sm font-semibold">User Query</Label>
                                        <Input
                                            id="query"
                                            placeholder="e.g., Eating 50g of carbs"
                                            value={query}
                                            onChange={(e) => setQuery(e.target.value)}
                                            className="bg-background/50 border-primary/10 focus-visible:ring-primary h-12"
                                        />
                                    </div>
                                    <div className="space-y-2">
                                        <Label htmlFor="glucose" className="text-sm font-semibold flex items-center gap-2">
                                            <Thermometer className="w-4 h-4 text-primary" /> Start Glucose (mg/dL)
                                        </Label>
                                        <Input
                                            id="glucose"
                                            type="number"
                                            value={glucose}
                                            onChange={(e) => setGlucose(e.target.value)}
                                            className="bg-background/50 border-primary/10 focus-visible:ring-primary h-12"
                                        />
                                    </div>
                                </div>
                                <Button
                                    type="submit"
                                    disabled={isLoading || !query.trim()}
                                    className="w-full h-14 text-lg font-bold group transition-all duration-500 rounded-xl"
                                >
                                    {isLoading ? (
                                        <Loader2 className="w-6 h-6 animate-spin mr-2" />
                                    ) : (
                                        <Send className="w-5 h-5 mr-2 group-hover:translate-x-1 group-hover:-translate-y-1 transition-transform duration-300" />
                                    )}
                                    {isLoading ? "Analyzing..." : "Run Analysis"}
                                </Button>
                            </form>
                        </CardContent>
                        <CardFooter className="bg-primary/[0.02] border-t border-primary/5 py-4">
                            <p className="text-[10px] text-center w-full uppercase tracking-widest text-muted-foreground opacity-70">
                                Local Intelligence Prototype v0.1
                            </p>
                        </CardFooter>
                    </Card>

                    {/* Visualization Panel */}
                    <Card className="lg:col-span-8 glass border-primary/5 shadow-2xl min-h-[500px] flex flex-col">
                        <CardHeader className="border-b border-primary/5 pb-4">
                            <CardTitle className="text-xl flex items-center gap-2">
                                <ChartIcon className="w-5 h-5 text-primary" />
                                Live Modeling
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="flex-1 flex flex-col p-8 items-center justify-center relative">
                            <AnimatePresence mode="wait">
                                {chartData ? (
                                    <motion.div
                                        key="chart"
                                        initial={{ opacity: 0, scale: 0.98 }}
                                        animate={{ opacity: 1, scale: 1 }}
                                        exit={{ opacity: 0, scale: 0.98 }}
                                        className="w-full h-[350px] space-y-8"
                                    >
                                        <div className="w-full h-[300px]">
                                            <ResponsiveContainer width="100%" height="100%">
                                                <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                                                    <defs>
                                                        <linearGradient id="colorGlucose" x1="0" y1="0" x2="0" y2="1">
                                                            <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                                                            <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                                                        </linearGradient>
                                                    </defs>
                                                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="rgba(255,255,255,0.05)" />
                                                    <XAxis
                                                        dataKey="time_mins"
                                                        hide
                                                    />
                                                    <YAxis
                                                        domain={[40, 400]}
                                                        axisLine={false}
                                                        tickLine={false}
                                                        tick={{ fontSize: 10, fill: 'rgba(255,255,255,0.5)' }}
                                                    />
                                                    <Tooltip content={<CustomTooltip />} />
                                                    <ReferenceLine y={180} stroke="#ef4444" strokeDasharray="3 3" strokeOpacity={0.5} label={{ position: 'right', value: 'High', fill: '#ef4444', fontSize: 10 }} />
                                                    <ReferenceLine y={70} stroke="#3b82f6" strokeDasharray="3 3" strokeOpacity={0.5} label={{ position: 'right', value: 'Low', fill: '#3b82f6', fontSize: 10 }} />
                                                    <Area
                                                        type="monotone"
                                                        dataKey="glucose"
                                                        stroke="#3b82f6"
                                                        strokeWidth={4}
                                                        fillOpacity={1}
                                                        fill="url(#colorGlucose)"
                                                        animationDuration={2000}
                                                    />
                                                </AreaChart>
                                            </ResponsiveContainer>
                                        </div>

                                        {/* Shortened Explanation Box */}
                                        {response && (
                                            <motion.div
                                                initial={{ opacity: 0, y: 10 }}
                                                animate={{ opacity: 1, y: 0 }}
                                                className="bg-primary/5 rounded-2xl p-6 border border-primary/10 relative"
                                            >
                                                <Quote className="absolute -top-3 -left-1 w-8 h-8 text-primary/20 fill-primary/10" />
                                                <p className="text-xl font-medium text-foreground text-center italic">
                                                    "{response}"
                                                </p>
                                            </motion.div>
                                        )}
                                    </motion.div>
                                ) : (
                                    <motion.div
                                        key="placeholder"
                                        className="text-center space-y-6 opacity-40 max-w-xs"
                                    >
                                        <div className="w-20 h-20 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-4 border border-dashed border-primary/30">
                                            <ChartIcon className="w-8 h-8 text-primary" />
                                        </div>
                                        <p className="text-lg">Enter a query to generate the digital twin projection.</p>
                                    </motion.div>
                                )}
                            </AnimatePresence>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </section>
    );
};
