"use client";
import ResumeForm from "@/components/ResumeForm";
import Header from "@/components/Header";

export default function UploadResumePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <Header />
      <div className="py-12">
        <ResumeForm />
      </div>
    </div>
  );
}
