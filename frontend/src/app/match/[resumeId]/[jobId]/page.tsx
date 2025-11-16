"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Header from "@/components/Header";
import MatchResult from "@/components/MatchResult";

type MatchResultData = {
  score: number;
  matched_skills: string[];
  missing_skills: string[];
  job_title?: string;
  resume_title?: string;
};

export default function MatchPage() {
  const { resumeId, jobId } = useParams();
  const [result, setResult] = useState<MatchResultData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const formData = new FormData();
    formData.append("resume_id", resumeId as string);
    formData.append("job_id", jobId as string);
    
    fetch("http://127.0.0.1:8000/match", {
      method: "POST",
      body: formData,
    })
      .then((res) => {
        if (!res.ok) throw new Error("Match failed");
        return res.json();
      })
      .then(setResult)
      .catch((err) => {
        console.error("Failed to get match result:", err);
        setResult({
          score: 0,
          matched_skills: [],
          missing_skills: ["Error occurred"],
          job_title: "Unknown Job",
          resume_title: "Unknown Resume"
        });
      })
      .finally(() => setLoading(false));
  }, [resumeId, jobId]);

  return (
    <div>
      <Header />
      {loading ? (
        <div className="p-6 max-w-2xl mx-auto text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p>Analyzing compatibility...</p>
        </div>
      ) : result ? (
        <MatchResult
          score={result.score}
          matchedSkills={result.matched_skills}
          missingSkills={result.missing_skills}
          jobTitle={result.job_title}
          resumeTitle={result.resume_title}
        />
      ) : (
        <div className="p-6 max-w-2xl mx-auto text-center">
          <p className="text-red-600">Failed to load match result</p>
        </div>
      )}
    </div>
  );
}
