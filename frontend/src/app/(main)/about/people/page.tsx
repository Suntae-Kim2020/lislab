'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { teamApi, TeamMember } from '@/lib/api/team';
import { Users } from 'lucide-react';

export default function PeoplePage() {
  const [members, setMembers] = useState<TeamMember[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    teamApi
      .getMembers()
      .then(setMembers)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="container mx-auto py-12 px-4">
      <div className="max-w-5xl mx-auto">
        {/* 헤더 */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Users className="h-8 w-8 text-primary" />
            <h1 className="text-4xl font-bold">LIS Lab 사람들</h1>
          </div>
          <p className="text-lg text-muted-foreground">
            LIS Lab을 함께 만들어가는 팀원들을 소개합니다.
          </p>
        </div>

        {loading ? (
          <div className="text-center py-12 text-muted-foreground">
            로딩 중...
          </div>
        ) : members.length === 0 ? (
          <div className="text-center py-12 text-muted-foreground">
            등록된 팀 멤버가 없습니다.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {members.map((member) => (
              <Card key={member.id} className="overflow-hidden">
                <CardContent className="pt-6 flex flex-col items-center text-center">
                  {/* 사진 */}
                  <div className="w-32 h-32 rounded-full overflow-hidden bg-muted mb-4 flex-shrink-0">
                    {member.photo ? (
                      <img
                        src={member.photo}
                        alt={member.name}
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center text-4xl text-muted-foreground">
                        {member.name.charAt(0)}
                      </div>
                    )}
                  </div>

                  {/* 이름 & 직함 */}
                  <h3 className="text-xl font-semibold">{member.name}</h3>
                  {member.title && (
                    <p className="text-sm text-muted-foreground mt-1">
                      {member.title}
                    </p>
                  )}

                  {/* 소개 */}
                  {member.bio && (
                    <p className="text-sm text-muted-foreground mt-3 leading-relaxed">
                      {member.bio}
                    </p>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
