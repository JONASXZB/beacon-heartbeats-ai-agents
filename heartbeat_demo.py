import tempfile
from pathlib import Path

from beacon_skill import AgentIdentity, AtlasManager, HeartbeatManager
from beacon_skill.codec import decode_envelopes, encode_envelope, verify_envelope


data_dir = Path(tempfile.mkdtemp(prefix="beacon_article_"))

identity = AgentIdentity.generate()
print(f"agent_id={identity.agent_id}")
print(f"public_key={identity.public_key_hex[:16]}...")

heartbeat = HeartbeatManager(data_dir=data_dir)
beat_result = heartbeat.beat(
    identity,
    status="alive",
    health={
        "queue_depth": 0,
        "jobs_completed": 3,
    },
)
beat = beat_result["heartbeat"]
print(f"heartbeat_status={beat['status']}")
print(f"heartbeat_count={beat['beat_count']}")

atlas = AtlasManager(data_dir=data_dir)
registration = atlas.register_agent(
    agent_id=identity.agent_id,
    domains=["coding", "ops"],
    name="article-demo-agent",
)
print(f"cities_joined={registration.get('cities_joined')}")

envelope_text = encode_envelope(
    {"kind": "hello", "text": "Beacon article demo"},
    version=2,
    identity=identity,
    include_pubkey=True,
)
decoded = decode_envelopes(envelope_text)[0]
print(f"envelope_verified={verify_envelope(decoded)}")
