from sqlalchemy import create_engine, text

e = create_engine("postgresql://igeta:igeta@localhost:5432/igeta_new")
with e.connect() as conn:
    cols = conn.execute(
        text(
            """
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = 'vi_factory3_stoc'
            ORDER BY ordinal_position
            """
        )
    ).all()
    print("columns:")
    for c in cols:
        print(c)
    viewdef = conn.execute(text("SELECT pg_get_viewdef('public.vi_factory3_stoc'::regclass, true)")).scalar()
    print("\nviewdef:\n", viewdef)
