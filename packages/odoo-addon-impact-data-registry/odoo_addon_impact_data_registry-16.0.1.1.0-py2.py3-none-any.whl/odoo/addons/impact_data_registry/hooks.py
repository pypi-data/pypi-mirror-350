from odoo import api, SUPERUSER_ID


def post_init_hook(cr, registry):
    """
    Create a trigger to prevent the creation of recursive categories directly
    in the database.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    env.cr.execute(
        """
        CREATE OR REPLACE FUNCTION prevent_impact_category_loop()
        RETURNS TRIGGER AS $$
        DECLARE
            ancestor_id INT;
        BEGIN
            IF NEW.parent_id IS NULL THEN RETURN NEW;
            END IF;
            IF NEW.parent_id IS NOT DISTINCT FROM OLD.parent_id THEN RETURN NEW;
            END IF;
            ancestor_id := NEW.parent_id;
            WHILE ancestor_id IS NOT NULL
            LOOP
                IF ancestor_id = NEW.id THEN
                    RAISE EXCEPTION 'You cannot create recursive categories.';
                END IF;
                SELECT parent_id INTO ancestor_id
                FROM impact_data_category
                WHERE id = ancestor_id;
            END LOOP;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        DROP TRIGGER IF EXISTS check_category_hierarchy ON impact_data_category;
        CREATE TRIGGER check_category_hierarchy
        BEFORE INSERT OR UPDATE ON impact_data_category
        FOR EACH ROW EXECUTE FUNCTION prevent_impact_category_loop();
        """
    )
