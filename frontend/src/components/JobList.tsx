"use client";

import { useState, useEffect } from "react";

type Job = {
  job_id: number;
  title: string;
  description: string;
  posted_at: string;
};

type JobListProps = {
  onJobSelect?: (jobId: number) => void;
};

export default function JobList({ onJobSelect }: JobListProps) {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/jobs")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch jobs");
        return res.json();
      })
      .then(setJobs)
      .catch((err) => {
        console.error("Failed to fetch jobs:", err);
        setError("Failed to load jobs");
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="p-4">Loading jobs...</div>;
  }

  if (error) {
    return <div className="p-4 text-red-600">{error}</div>;
  }

  return (
    <div className="space-y-4">
      {jobs.map((job) => (
        <div key={job.job_id} className="border p-4 rounded-lg shadow-sm">
          <h3 className="text-xl font-semibold mb-2">{job.title}</h3>
          <p className="text-gray-600 mb-3">{job.description}</p>
          <div className="flex gap-2">
            <a
              href={`/match/1/${job.job_id}`}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Check Compatibility
            </a>
            {onJobSelect && (
              <button
                onClick={() => onJobSelect(job.job_id)}
                className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700"
              >
                Select Job
              </button>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
