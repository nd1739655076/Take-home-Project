import { useState, useEffect } from "react";
import LayoutRenderer from "../components/LayoutRenderer";
import Navbar from "../components/Navbar";

export default function Home() {
    const [question, setQuestion] = useState("");
    const [responseData, setResponseData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [conversation, setConversation] = useState([]);
    const [hasAsked, setHasAsked] = useState(false);

    useEffect(() => {
        if (hasAsked) {
            window.scrollTo({ top: 0, behavior: "smooth" });
        }
    }, [hasAsked]);

    useEffect(() => {
        if (responseData) {
            console.log(" Response Data:", responseData);
        }
    }, [responseData]);

    const handleAsk = async () => {
        if (!question.trim()) return;

        const userMessage = { type: "user", content: question };
        setConversation((prev) => [...prev, userMessage]);
        setQuestion("");
        setLoading(true);
        setResponseData(null);
        setHasAsked(true);

        try {
            const res = await fetch("http://localhost:8000/ask", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question }),
            });

            const data = await res.json();
            const botMessage = { type: "bot", content: data };
            setConversation((prev) => [...prev, botMessage]);
            setResponseData(data);
        } catch (err) {
            alert("Failed to get answer.");
        }

        setLoading(false);
    };

    return (
        <div className="min-h-screen bg-gray-50 flex flex-col pb-28">
            <Navbar />

            {/* header */}
            <div className="flex-1 flex flex-col justify-start items-center px-4 pt-8">
                {!hasAsked && (
                    <div className="text-center mb-8">
                        <h1 className="text-3xl font-bold text-blue-600">
                            Ask Me About <span className="text-blue-800">"The Great Gatsby"</span>
                        </h1>
                        <p className="text-sm text-gray-600 mt-2">
                            Type a question about character, symbols, or plot points from the novel
                        </p>
                    </div>
                )}

                {/* example prompts */}
                {!hasAsked && (
                    <div className="flex flex-wrap justify-center gap-4 mb-10">
                        {[
                            "Tell me about Gatsby’s life and experiences",
                            "Tell me about the women characters in the book",
                            "What are the major symbols in The Great Gatsby",
                        ].map((q, idx) => (
                            <button
                                key={idx}
                                onClick={() => setQuestion(q)}
                                className="bg-white px-4 py-3 rounded-lg shadow hover:bg-blue-50 text-sm text-gray-700 border w-64 text-left"
                            >
                                <span className="block text-blue-700 font-semibold">Ask about:</span>
                                <span className="block mt-1 text-gray-800 italic">“{q}”</span>
                            </button>
                        ))}
                    </div>
                )}

                {/* chat history */}
                <div className="w-full max-w-5xl space-y-6">
                    {conversation.map((item, index) =>
                        item.type === "user" ? (
                            <div key={index} className="text-right">
                                <div className="inline-block bg-white text-gray-900 px-4 py-2 rounded-2xl shadow-md text-base font-sans">
                                    {item.content}
                                </div>
                            </div>
                        ) : (
                            <div key={index} className="text-left">
                                <LayoutRenderer layout={item.content.layout} data={item.content} />
                            </div>
                        )
                    )}
                    {loading && (
                        <p className="text-center text-gray-500 text-sm">Thinking...</p>
                    )}
                </div>
            </div>

            {/* input */}
            <div className="fixed bottom-0 left-0 w-full bg-gray-50 py-4 px-4 border-t shadow-inner z-10">
                <div className="max-w-xl mx-auto flex items-center gap-2">
                    <input
                        type="text"
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                        onKeyDown={(e) => e.key === "Enter" && handleAsk()}
                        placeholder="Ask a question about the book..."
                        className="flex-1 p-3 rounded-full border border-gray-300 shadow-sm text-sm font-sans"
                    />
                    <button
                        onClick={handleAsk}
                        className="bg-blue-600 text-white px-4 py-3 rounded-full hover:bg-blue-700 transition"
                    >
                        ➤
                    </button>
                </div>
            </div>
        </div>
    );
}
