import { NextResponse } from 'next/server';
import { sql } from '@/lib/db'; // 아까 만든 db 설정 파일
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY, // .env.local에 저장 필요
});

export async function GET() {
  try {
    // 1. OpenAI 연동 체크
    const completion = await openai.chat.completions.create({
      messages: [{ role: "user", content: "Say 'Success' if you can read this." }],
      model: "gpt-3.5-turbo",
    });
    const aiResponse = completion.choices[0].message.content;

    // 2. DB 연동 및 저장 체크
    // (테스트를 위해 간단한 테이블이 있다고 가정하거나, 단순 쿼리 실행)
    await sql`
      CREATE TABLE IF NOT EXISTS test_logs (
        id SERIAL PRIMARY KEY,
        content TEXT,
        created_at TIMESTAMP DEFAULT NOW()
      )
    `;
    
    await sql`INSERT INTO test_logs (content) VALUES (${aiResponse})`;

    // 3. 결과 확인을 위해 DB 데이터 다시 조회
    const logs = await sql`SELECT * FROM test_logs ORDER BY created_at DESC LIMIT 1`;

    return NextResponse.json({ 
      status: "All systems go!",
      openai_said: aiResponse,
      db_saved_data: logs[0]
    });

  } catch (error) {
    console.error("Error details:", error);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}