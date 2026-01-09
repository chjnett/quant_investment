# 프론트엔드 도커파일
FROM node:20-alpine AS base

# 필요한 의존성만 딱 설치함
FROM base AS deps
WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

# 소스 코드가 바뀔 때만 다시 빌드함
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# 빌드할 때 Next.js 텔레메트리 끔
ENV NEXT_TELEMETRY_DISABLED 1

RUN npm run build

# 실제 프로덕션 이미지, 필요한 파일만 복사해서 실행함
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# COPY --from=builder /app/public ./public

# 이미지 크기 줄이려고 output traces 자동 활용함
# 참고: https://nextjs.org/docs/advanced-features/output-file-tracing
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000

CMD ["node", "server.js"]
