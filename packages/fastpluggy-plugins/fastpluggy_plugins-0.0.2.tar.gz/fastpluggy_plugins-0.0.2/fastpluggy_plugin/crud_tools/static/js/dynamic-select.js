/**
 * Binds a dynamic select field to another field's change event.
 *
 * @param {string} triggerFieldId - The ID of the source field (e.g. 'user_id')
 * @param {string} targetFieldId - The ID of the field to update (e.g. 'project_id')
 * @param {string} urlTemplate - The URL template (e.g. '/dynamic-select/Project/project_id?value={user_id}')
 * @param {string} placeholderText - Optional placeholder for the select field
 */
function bindDynamicSelect(triggerFieldId, targetFieldId, urlTemplate, placeholderText = 'Select an option') {
    const trigger = document.getElementById(triggerFieldId);
    const target = document.getElementById(targetFieldId);

    if (!trigger || !target) {
        console.warn(`[DynamicSelect] Could not find fields: ${triggerFieldId} or ${targetFieldId}`);
        return;
    }

    trigger.addEventListener('change', () => {
        const value = trigger.value;
        const url = urlTemplate.replace(`{${triggerFieldId}}`, encodeURIComponent(value));

        fetch(url)
            .then(res => res.json())
            .then(data => {
                // Always clean the select
                target.innerHTML = '';

                if (data.length === 0) {
                    const opt = document.createElement('option');
                    opt.disabled = true;
                    opt.selected = true;
                    opt.textContent = 'No results found';
                    target.appendChild(opt);
                    return;
                }

                // Add real options
                data.forEach(item => {
                    const opt = document.createElement('option');
                    opt.value = item.id;
                    opt.textContent = item.name;
                    target.appendChild(opt);
                });

                // Reset the field selection
                target.value = '';
                target.dispatchEvent(new Event('change'));
            })
            .catch(err => {
                console.error(`[DynamicSelect] Error loading ${targetFieldId} from`, url, err);
            });
    });
}
